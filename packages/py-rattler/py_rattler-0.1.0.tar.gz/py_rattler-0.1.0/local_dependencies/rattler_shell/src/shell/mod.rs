//! This module contains the [`Shell`] trait and implementations for various shells.

use crate::activation::PathModificationBehavior;
use enum_dispatch::enum_dispatch;
use itertools::Itertools;
use rattler_conda_types::Platform;
use std::collections::HashMap;
use std::process::Command;
use std::str::FromStr;
use std::{
    fmt::Write,
    path::{Path, PathBuf},
};
use thiserror::Error;

/// A trait for generating shell scripts.
/// The trait is implemented for each shell individually.
///
/// # Example
///
/// ```
/// use std::path::PathBuf;
/// use rattler_shell::shell::Bash;
/// use rattler_shell::shell::Shell;
///
/// let mut script = String::new();
/// let shell = Bash;
/// shell.set_env_var(&mut script, "FOO", "bar").unwrap();
///
/// assert_eq!(script, "export FOO=\"bar\"\n");
/// ```
#[enum_dispatch(ShellEnum)]
pub trait Shell {
    /// Set an env var by `export`-ing it.
    fn set_env_var(&self, f: &mut impl Write, env_var: &str, value: &str) -> std::fmt::Result;

    /// Unset an env var by `unset`-ing it.
    fn unset_env_var(&self, f: &mut impl Write, env_var: &str) -> std::fmt::Result;

    /// Run a script in the current shell.
    fn run_script(&self, f: &mut impl Write, path: &Path) -> std::fmt::Result;

    /// Executes a command in the current shell. Use [`Self::run_script`] when you want to run
    /// another shell script.
    fn run_command<'a>(
        &self,
        f: &mut impl Write,
        command: impl IntoIterator<Item = &'a str> + 'a,
    ) -> std::fmt::Result {
        writeln!(f, "{}", command.into_iter().join(" "))
    }

    /// Set the PATH variable to the given paths.
    fn set_path(
        &self,
        f: &mut impl Write,
        paths: &[PathBuf],
        modification_behaviour: PathModificationBehavior,
        platform: &Platform,
    ) -> std::fmt::Result {
        let mut paths_vec = paths
            .iter()
            .map(|path| path.to_string_lossy().into_owned())
            .collect_vec();
        // Replace, Append, or Prepend the path variable to the paths.
        match modification_behaviour {
            PathModificationBehavior::Replace => (),
            PathModificationBehavior::Append => paths_vec.insert(0, self.format_env_var("PATH")),
            PathModificationBehavior::Prepend => paths_vec.push(self.format_env_var("PATH")),
        }
        // Create the shell specific list of paths.
        let paths_string = paths_vec.join(self.path_seperator(platform));

        self.set_env_var(f, "PATH", paths_string.as_str())
    }

    /// The extension that shell scripts for this interpreter usually use.
    fn extension(&self) -> &str;

    /// The executable that can be called to start this shell.
    fn executable(&self) -> &str;

    /// Constructs a [`Command`] that will execute the specified script by this shell.
    fn create_run_script_command(&self, path: &Path) -> Command;

    /// Path seperator
    fn path_seperator(&self, platform: &Platform) -> &str {
        if platform.is_unix() {
            ":"
        } else {
            ";"
        }
    }

    /// Format the environment variable for the shell.
    fn format_env_var(&self, var_name: &str) -> String {
        format!("${{{var_name}}}")
    }

    /// Emits echoing certain text to stdout.
    fn echo(&self, f: &mut impl Write, text: &str) -> std::fmt::Result {
        writeln!(f, "echo {}", shlex::quote(text))
    }

    /// Emits writing all current environment variables to stdout.
    fn env(&self, f: &mut impl Write) -> std::fmt::Result {
        writeln!(f, "/usr/bin/env")
    }

    /// Parses environment variables emitted by the `Shell::env` command.
    fn parse_env<'i>(&self, env: &'i str) -> HashMap<&'i str, &'i str> {
        env.lines()
            .filter_map(|line| line.split_once('='))
            .collect()
    }
}

/// Convert a native PATH on Windows to a Unix style path usign cygpath.
fn native_path_to_unix(path: &str) -> Result<String, std::io::Error> {
    // call cygpath on Windows to convert paths to Unix style
    let output = Command::new("cygpath")
        .arg("--unix")
        .arg("--path")
        .arg(path)
        .output();

    match output {
        Ok(output) if output.status.success() => Ok(String::from_utf8(output.stdout)
            .map_err(|_| {
                std::io::Error::new(
                    std::io::ErrorKind::Other,
                    "failed to convert path to Unix style",
                )
            })?
            .trim()
            .to_string()),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Err(e),
        Err(e) => Err(std::io::Error::new(
            std::io::ErrorKind::Other,
            format!("failed to convert path to Unix style: {e}"),
        )),
        _ => Err(std::io::Error::new(
            std::io::ErrorKind::Other,
            "failed to convert path to Unix style: cygpath failed",
        )),
    }
}

/// A [`Shell`] implementation for the Bash shell.
#[derive(Debug, Clone, Copy, Default)]
pub struct Bash;

impl Shell for Bash {
    fn set_env_var(&self, f: &mut impl Write, env_var: &str, value: &str) -> std::fmt::Result {
        writeln!(f, "export {}=\"{}\"", env_var, value)
    }

    fn unset_env_var(&self, f: &mut impl Write, env_var: &str) -> std::fmt::Result {
        writeln!(f, "unset {}", env_var)
    }

    fn run_script(&self, f: &mut impl Write, path: &Path) -> std::fmt::Result {
        writeln!(f, ". \"{}\"", path.to_string_lossy())
    }

    fn set_path(
        &self,
        f: &mut impl Write,
        paths: &[PathBuf],
        modification_behaviour: PathModificationBehavior,
        platform: &Platform,
    ) -> std::fmt::Result {
        // Put paths in a vector of the correct format.
        let mut paths_vec = paths
            .iter()
            .map(|path| {
                // check if we are on Windows, and if yes, convert native path to unix for (Git) Bash
                if cfg!(windows) {
                    match native_path_to_unix(path.to_string_lossy().as_ref()) {
                        Ok(path) => path,
                        Err(e) if e.kind() == std::io::ErrorKind::NotFound => {
                            // This indicates that the cypath executable could not be found. In that
                            // case we just ignore any conversion and use the windows path directly.
                            path.to_string_lossy().to_string()
                        }
                        Err(e) => panic!("{e}"),
                    }
                } else {
                    path.to_string_lossy().into_owned()
                }
            })
            .collect_vec();

        // Replace, Append, or Prepend the path variable to the paths.
        match modification_behaviour {
            PathModificationBehavior::Replace => (),
            PathModificationBehavior::Prepend => paths_vec.push(self.format_env_var("PATH")),
            PathModificationBehavior::Append => paths_vec.insert(0, self.format_env_var("PATH")),
        }
        // Create the shell specific list of paths.
        let paths_string = paths_vec.join(self.path_seperator(platform));

        self.set_env_var(f, "PATH", paths_string.as_str())
    }

    fn extension(&self) -> &str {
        "sh"
    }

    fn executable(&self) -> &str {
        "bash"
    }

    fn create_run_script_command(&self, path: &Path) -> Command {
        let mut cmd = Command::new(self.executable());

        // check if we are on Windows, and if yes, convert native path to unix for (Git) Bash
        if cfg!(windows) {
            cmd.arg(native_path_to_unix(path.to_str().unwrap()).unwrap());
        } else {
            cmd.arg(path);
        }

        cmd
    }
}

/// A [`Shell`] implementation for the Zsh shell.
#[derive(Debug, Clone, Copy, Default)]
pub struct Zsh;

impl Shell for Zsh {
    fn set_env_var(&self, f: &mut impl Write, env_var: &str, value: &str) -> std::fmt::Result {
        writeln!(f, "export {}=\"{}\"", env_var, value)
    }

    fn unset_env_var(&self, f: &mut impl Write, env_var: &str) -> std::fmt::Result {
        writeln!(f, "unset {}", env_var)
    }

    fn run_script(&self, f: &mut impl Write, path: &Path) -> std::fmt::Result {
        writeln!(f, ". \"{}\"", path.to_string_lossy())
    }

    fn extension(&self) -> &str {
        "sh"
    }

    fn executable(&self) -> &str {
        "zsh"
    }

    fn create_run_script_command(&self, path: &Path) -> Command {
        let mut cmd = Command::new(self.executable());
        cmd.arg(path);
        cmd
    }
}

/// A [`Shell`] implementation for the Xonsh shell.
#[derive(Debug, Clone, Copy, Default)]
pub struct Xonsh;

impl Shell for Xonsh {
    fn set_env_var(&self, f: &mut impl Write, env_var: &str, value: &str) -> std::fmt::Result {
        writeln!(f, "${} = \"{}\"", env_var, value)
    }

    fn unset_env_var(&self, f: &mut impl Write, env_var: &str) -> std::fmt::Result {
        writeln!(f, "del ${}", env_var)
    }

    fn run_script(&self, f: &mut impl Write, path: &Path) -> std::fmt::Result {
        writeln!(f, "source-bash \"{}\"", path.to_string_lossy())
    }

    fn extension(&self) -> &str {
        "sh"
    }

    fn executable(&self) -> &str {
        "xonsh"
    }

    fn create_run_script_command(&self, path: &Path) -> Command {
        let mut cmd = Command::new(self.executable());
        cmd.arg(path);
        cmd
    }
}

/// A [`Shell`] implementation for the cmd.exe shell.
#[derive(Debug, Clone, Copy, Default)]
pub struct CmdExe;

impl Shell for CmdExe {
    fn set_env_var(&self, f: &mut impl Write, env_var: &str, value: &str) -> std::fmt::Result {
        writeln!(f, "@SET \"{}={}\"", env_var, value)
    }

    fn unset_env_var(&self, f: &mut impl Write, env_var: &str) -> std::fmt::Result {
        writeln!(f, "@SET {}=", env_var)
    }

    fn run_script(&self, f: &mut impl Write, path: &Path) -> std::fmt::Result {
        writeln!(f, "@CALL \"{}\"", path.to_string_lossy())
    }

    fn run_command<'a>(
        &self,
        f: &mut impl Write,
        command: impl IntoIterator<Item = &'a str> + 'a,
    ) -> std::fmt::Result {
        writeln!(f, "@{}", command.into_iter().join(" "))
    }

    fn extension(&self) -> &str {
        "bat"
    }

    fn executable(&self) -> &str {
        "cmd.exe"
    }

    fn create_run_script_command(&self, path: &Path) -> Command {
        let mut cmd = Command::new(self.executable());
        cmd.arg("/D").arg("/C").arg(path);
        cmd
    }

    fn format_env_var(&self, var_name: &str) -> String {
        format!("%{var_name}%")
    }

    fn echo(&self, f: &mut impl Write, text: &str) -> std::fmt::Result {
        writeln!(f, "@ECHO {}", shlex::quote(text))
    }

    /// Emits writing all current environment variables to stdout.
    fn env(&self, f: &mut impl Write) -> std::fmt::Result {
        writeln!(f, "@SET")
    }
}

/// A [`Shell`] implementation for PowerShell.
#[derive(Debug, Clone, Default)]
pub struct PowerShell {
    executable_path: Option<String>,
}

impl Shell for PowerShell {
    fn set_env_var(&self, f: &mut impl Write, env_var: &str, value: &str) -> std::fmt::Result {
        writeln!(f, "${{Env:{}}} = \"{}\"", env_var, value)
    }

    fn unset_env_var(&self, f: &mut impl Write, env_var: &str) -> std::fmt::Result {
        writeln!(f, "${{Env:{}}}=\"\"", env_var)
    }

    fn run_script(&self, f: &mut impl Write, path: &Path) -> std::fmt::Result {
        writeln!(f, ". \"{}\"", path.to_string_lossy())
    }

    fn extension(&self) -> &str {
        "ps1"
    }

    fn executable(&self) -> &str {
        self.executable_path.as_deref().unwrap_or("pwsh")
    }

    fn create_run_script_command(&self, path: &Path) -> Command {
        let mut cmd = Command::new(self.executable());
        cmd.arg(path);
        cmd
    }

    fn format_env_var(&self, var_name: &str) -> String {
        format!("$Env:{var_name}")
    }

    /// Emits writing all current environment variables to stdout.
    fn env(&self, f: &mut impl Write) -> std::fmt::Result {
        writeln!(f, r##"dir env: | %{{"{{0}}={{1}}" -f $_.Name,$_.Value}}"##)
    }
}

/// A [`Shell`] implementation for the Fish shell.
#[derive(Debug, Clone, Copy, Default)]
pub struct Fish;

impl Shell for Fish {
    fn set_env_var(&self, f: &mut impl Write, env_var: &str, value: &str) -> std::fmt::Result {
        writeln!(f, "set -gx {} \"{}\"", env_var, value)
    }

    fn format_env_var(&self, var_name: &str) -> String {
        // Fish doesnt want the extra brackets '{}'
        format!("${var_name}")
    }

    fn unset_env_var(&self, f: &mut impl Write, env_var: &str) -> std::fmt::Result {
        writeln!(f, "set -e {}", env_var)
    }

    fn run_script(&self, f: &mut impl Write, path: &Path) -> std::fmt::Result {
        writeln!(f, "source \"{}\"", path.to_string_lossy())
    }

    fn extension(&self) -> &str {
        "fish"
    }

    fn executable(&self) -> &str {
        "fish"
    }

    fn create_run_script_command(&self, path: &Path) -> Command {
        let mut cmd = Command::new(self.executable());
        cmd.arg(path);
        cmd
    }
}

fn escape_backslashes(s: &str) -> String {
    s.replace('\\', "\\\\")
}

/// A [`Shell`] implementation for the Bash shell.
#[derive(Debug, Clone, Copy, Default)]
pub struct NuShell;

impl Shell for NuShell {
    fn set_env_var(&self, f: &mut impl Write, env_var: &str, value: &str) -> std::fmt::Result {
        // escape backslashes for Windows (make them double backslashes)
        writeln!(f, "$env.{} = \"{}\"", env_var, escape_backslashes(value))
    }

    fn unset_env_var(&self, f: &mut impl Write, env_var: &str) -> std::fmt::Result {
        writeln!(f, "hide-env {}", env_var)
    }

    fn run_script(&self, f: &mut impl Write, path: &Path) -> std::fmt::Result {
        writeln!(f, "source \"{}\"", path.to_string_lossy())
    }

    fn set_path(
        &self,
        f: &mut impl Write,
        paths: &[PathBuf],
        modification_behaviour: PathModificationBehavior,
        _platform: &Platform,
    ) -> std::fmt::Result {
        let path = paths
            .iter()
            .map(|path| escape_backslashes(&format!("\"{}\"", path.to_string_lossy().into_owned())))
            .join(", ");

        // Replace, Append, or Prepend the path variable to the paths.
        match modification_behaviour {
            PathModificationBehavior::Replace => {
                writeln!(f, "$env.PATH = [{}]", path)
            }
            PathModificationBehavior::Prepend => {
                writeln!(f, "$env.PATH = ($env.PATH | prepend [{}])", path)
            }
            PathModificationBehavior::Append => {
                writeln!(f, "$env.PATH = ($env.PATH | append [{}])", path)
            }
        }
    }

    fn extension(&self) -> &str {
        "nu"
    }

    fn executable(&self) -> &str {
        "nu"
    }

    fn create_run_script_command(&self, path: &Path) -> Command {
        let mut cmd = Command::new(self.executable());
        cmd.arg(path);
        cmd
    }
}

/// A generic [`Shell`] implementation for concrete shell types.
#[enum_dispatch]
#[allow(missing_docs)]
#[derive(Clone, Debug)]
pub enum ShellEnum {
    Bash,
    Zsh,
    Xonsh,
    CmdExe,
    PowerShell,
    Fish,
    NuShell,
}

// The default shell is determined by the current OS.
impl Default for ShellEnum {
    fn default() -> Self {
        if cfg!(windows) {
            CmdExe.into()
        } else {
            Bash.into()
        }
    }
}

impl ShellEnum {
    /// Parse a shell from a path to the executable for the shell.
    pub fn from_shell_path<P: AsRef<Path>>(path: P) -> Option<Self> {
        parse_shell_from_path(path.as_ref())
    }

    /// Determine the user's current shell from the environment
    ///
    /// This will read the SHELL environment variable and try to determine which shell is in use
    /// from that.
    ///
    /// If SHELL is set, but contains a value that doesn't correspond to one of the supported shell
    /// types, then return `None`.
    pub fn from_env() -> Option<Self> {
        if let Some(env_shell) = std::env::var_os("SHELL") {
            Self::from_shell_path(env_shell)
        } else if cfg!(windows) {
            Some(PowerShell::default().into())
        } else {
            None
        }
    }

    /// Guesses the current shell by checking the name of the parent process.
    #[cfg(feature = "sysinfo")]
    pub fn from_parent_process() -> Option<Self> {
        use sysinfo::{get_current_pid, ProcessExt, SystemExt};

        let mut system_info = sysinfo::System::new();

        // Get current process information
        let current_pid = get_current_pid().ok()?;
        system_info.refresh_process(current_pid);
        let parent_process_id = system_info
            .process(current_pid)
            .and_then(|process| process.parent())?;

        // Get the name of the parent process
        system_info.refresh_process(parent_process_id);
        let parent_process = system_info.process(parent_process_id)?;
        let parent_process_name = parent_process.name().to_lowercase();

        tracing::debug!(
            "Guessing ShellEnum. Parent process name: {} and args: {:?}",
            &parent_process_name,
            &parent_process.cmd()
        );

        if parent_process_name.contains("bash") {
            Some(Bash.into())
        } else if parent_process_name.contains("zsh") {
            Some(Zsh.into())
        } else if parent_process_name.contains("xonsh")
            // xonsh is a python shell, so we need to check if the parent process is python and if it
            // contains xonsh in the arguments.
            || (parent_process_name.contains("python")
                && parent_process
                    .cmd().iter()
                    .any(|arg| arg.contains("xonsh")))
        {
            Some(Xonsh.into())
        } else if parent_process_name.contains("fish") {
            Some(Fish.into())
        } else if parent_process_name.contains("nu") {
            Some(NuShell.into())
        } else if parent_process_name.contains("powershell") || parent_process_name.contains("pwsh")
        {
            Some(
                PowerShell {
                    executable_path: Some(parent_process_name),
                }
                .into(),
            )
        } else if parent_process_name.contains("cmd.exe") {
            Some(CmdExe.into())
        } else {
            None
        }
    }
}

/// Parsing of a shell was not possible. The shell mostlikely is not supported.
#[derive(Debug, Error)]
#[error("{0}")]
pub struct ParseShellEnumError(String);

impl FromStr for ShellEnum {
    type Err = ParseShellEnumError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "bash" => Ok(Bash.into()),
            "zsh" => Ok(Zsh.into()),
            "xonsh" => Ok(Xonsh.into()),
            "fish" => Ok(Fish.into()),
            "cmd" => Ok(CmdExe.into()),
            "nu" | "nushell" => Ok(NuShell.into()),
            "powershell" | "powershell_ise" => Ok(PowerShell::default().into()),
            _ => Err(ParseShellEnumError(format!(
                "'{}' is an unknown shell variant",
                s
            ))),
        }
    }
}

/// Determine the shell from a path to a shell.
fn parse_shell_from_path(path: &Path) -> Option<ShellEnum> {
    let name = path.file_stem()?.to_str()?;
    ShellEnum::from_str(name).ok()
}

/// A helper struct for generating shell scripts.
pub struct ShellScript<T: Shell> {
    /// The shell class to generate the script for.
    shell: T,
    /// The contents of the script.
    pub contents: String,
    /// The platform for which the script will be generated
    platform: Platform,
}

impl<T: Shell> ShellScript<T> {
    /// Create a new [`ShellScript`] for the given shell.
    pub fn new(shell: T, platform: Platform) -> Self {
        Self {
            shell,
            contents: String::new(),
            platform,
        }
    }

    /// Export an environment variable.
    pub fn set_env_var(&mut self, env_var: &str, value: &str) -> &mut Self {
        self.shell
            .set_env_var(&mut self.contents, env_var, value)
            .unwrap();
        self
    }

    /// Unset an environment variable.
    pub fn unset_env_var(&mut self, env_var: &str) -> &mut Self {
        self.shell
            .unset_env_var(&mut self.contents, env_var)
            .unwrap();
        self
    }

    /// Set the PATH environment variable to the given paths.
    pub fn set_path(
        &mut self,
        paths: &[PathBuf],
        path_modification_behavior: PathModificationBehavior,
    ) -> &mut Self {
        self.shell
            .set_path(
                &mut self.contents,
                paths,
                path_modification_behavior,
                &self.platform,
            )
            .unwrap();
        self
    }

    /// Run a script in the generated shell script.
    pub fn run_script(&mut self, path: &Path) -> &mut Self {
        self.shell.run_script(&mut self.contents, path).unwrap();
        self
    }
}

#[cfg(test)]
mod tests {
    use std::str::FromStr;

    use super::*;

    #[test]
    fn test_bash() {
        let mut script = ShellScript::new(Bash, Platform::Linux64);

        script
            .set_env_var("FOO", "bar")
            .unset_env_var("FOO")
            .run_script(&PathBuf::from_str("foo.sh").expect("blah"));

        insta::assert_snapshot!(script.contents);
    }

    #[test]
    fn test_fish() {
        let mut script = ShellScript::new(Fish, Platform::Linux64);

        script
            .set_env_var("FOO", "bar")
            .unset_env_var("FOO")
            .run_script(&PathBuf::from_str("foo.sh").expect("blah"));

        insta::assert_snapshot!(script.contents);
    }

    #[cfg(feature = "sysinfo")]
    #[test]
    fn test_from_parent_process_doenst_crash() {
        let shell = ShellEnum::from_parent_process();
        println!("Detected shell: {:?}", shell);
    }

    #[test]
    fn test_from_env() {
        let shell = ShellEnum::from_env();
        println!("Detected shell: {:?}", shell);
    }

    #[test]
    fn test_path_seperator() {
        let mut script = ShellScript::new(Bash, Platform::Linux64);
        script.set_path(
            &[PathBuf::from("/foo"), PathBuf::from("/bar")],
            PathModificationBehavior::Prepend,
        );
        assert!(script.contents.contains("/foo:/bar"));

        let mut script = ShellScript::new(Bash, Platform::Win64);
        script.set_path(
            &[PathBuf::from("/foo"), PathBuf::from("/bar")],
            PathModificationBehavior::Prepend,
        );
        assert!(script.contents.contains("/foo;/bar"));
    }
}
