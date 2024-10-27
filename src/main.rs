use std::process::{Command, exit};
use std::path::Path;

fn print_header(message: &str) {
    println!("\n{}", "=".repeat(50));
    println!("{}", format!(" {} ", message).pad_to_center(50, '='));
    println!("{}\n", "=".repeat(50));
}

fn print_step(message: &str) {
    println!(">> {}", message);
}

fn run_command(command: &str, args: &[&str]) -> Result<(), String> {
    let status = Command::new(command)
    .args(args)
    .status()
    .map_err(|e| format!("Failed to execute command: {}", e))?;

    if status.success() {
        Ok(())
    } else {
        Err(format!("Command failed with exit code: {:?}", status.code()))
    }
}

fn detect_platform() -> String {
    if cfg!(target_os = "windows") {
        "windows".to_string()
    } else if cfg!(target_os = "macos") {
        "mac".to_string()
    } else if cfg!(target_os = "linux") {
        "linux".to_string()
    } else {
        eprintln!("Unsupported platform");
        exit(1);
    }
}

fn setup_conda_env() -> Result<(), String> {
    print_step("Setting up Conda environment 'H2LooP-T-data'...");
    run_command("conda", &["create", "-n", "H2LooP-T-data", "python=3.9", "-y"])?;
    Ok(())
}

fn install_tesseract(platform: &str) -> Result<(), String> {
    print_step("Installing Tesseract OCR...");
    match platform {
        "mac" => run_command("brew", &["install", "tesseract"])?,
        "windows" => run_command("conda", &["install", "-c", "conda-forge", "tesseract", "-y"])?,
        "linux" => {
            run_command("sudo", &["apt-get", "update"])?;
            run_command("sudo", &["apt-get", "install", "-y", "tesseract-ocr"])?;
        },
        _ => return Err("Unsupported platform".to_string()),
    }
    Ok(())
}

fn install_python_requirements() -> Result<(), String> {
    print_step("Installing Python requirements...");
    let requirements = [
        "python-dotenv==1.0.0", "openai==0.27.6", "pyfiglet==0.8.post1",
        "unstructured==0.6.1", "numpy==1.24.3", "pandas==2.0.3",
        "requests==2.31.0", "PyMuPDF==1.22.3", "pdf2image==1.16.3",
        "pytesseract==0.3.10", "pillow==10.0.0", "matplotlib==3.7.1",
        "torch==2.0.1", "opencv-python==4.7.0.72", "nltk==3.8.1",
        "pdfminer.six==20221105", "unstructured_inference==0.4.10"
    ];

    for req in &requirements {
        run_command("pip", &["install", req])?;
    }
    Ok(())
}

fn verify_installation() -> Result<(), String> {
    print_step("Verifying installation...");
    let checks = [
        ("python", vec!["--version"]),
        ("conda", vec!["--version"]),
        ("tesseract", vec!["--version"]),
        ("pip", vec!["list"]),
    ];

    for (cmd, args) in &checks {
        match run_command(cmd, &args) {
            Ok(_) => println!("✓ {} is installed", cmd),
            Err(_) => println!("✗ {} is not installed or not working properly", cmd),
        }
    }
    Ok(())
}

trait PadToCenter {
    fn pad_to_center(&self, width: usize, pad_char: char) -> String;
}

impl PadToCenter for str {
    fn pad_to_center(&self, width: usize, pad_char: char) -> String {
        let len = self.len();
        if len >= width {
            self.to_string()
        } else {
            let left_pad = (width - len) / 2;
            let right_pad = width - len - left_pad;
            format!("{}{}{}", pad_char.to_string().repeat(left_pad), self, pad_char.to_string().repeat(right_pad))
        }
    }
}

fn main() -> Result<(), String> {
    print_header("H2LooP-T-data Setup Script");

    let platform = detect_platform();
    print_step(&format!("Detected platform: {}", platform));

    setup_conda_env()?;
    run_command("conda", &["activate", "H2LooP-T-data"])?;
    install_tesseract(&platform)?;
    install_python_requirements()?;
    verify_installation()?;

    print_header("Setup Complete!");
    print_step("Passing execution to main.py...");

    // Pass execution to main.py
    let main_script = Path::new("main.py");
    if main_script.exists() {
        run_command("python", &[main_script.to_str().unwrap()])?;
    } else {
        println!("Error: main.py not found in the current directory.");
    }

    Ok(())
}
