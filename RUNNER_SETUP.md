# GitHub Actions Runner Installation Guide

This guide explains how to use the `install-github-runner.sh` script to set up a GitHub Actions self-hosted runner on Linux or macOS systems.

## Prerequisites

- **Operating System**: Linux or macOS
- **Architecture**: x64, ARM64, or ARM (armv7l)
- **Permissions**:
  - Standard user access for runner installation
  - `sudo` access for service installation (Linux only)
- **Network Access**: Ability to reach GitHub APIs and download releases
- **GitHub Token**: A runner registration token from your repository or organization

## Getting a Runner Registration Token

1. For a **repository**:
   - Go to your repository on GitHub
   - Navigate to: Settings → Actions → Runners
   - Click "New self-hosted runner"
   - Copy the token from the configuration command

2. For an **organization**:
   - Go to your organization on GitHub
   - Navigate to: Settings → Actions → Runners
   - Click "New runner" → "New self-hosted runner"
   - Copy the token from the configuration command

**Note**: Tokens expire quickly (typically 1 hour), so generate them right before running the installation script.

## Basic Usage

### Minimum Required Arguments

```bash
./install-github-runner.sh \
  --url https://github.com/your-org/your-repo \
  --token YOUR_REGISTRATION_TOKEN
```

### Full Example with Options

```bash
./install-github-runner.sh \
  --url https://github.com/your-org/your-repo \
  --token YOUR_REGISTRATION_TOKEN \
  --name my-custom-runner \
  --labels self-hosted,linux,gpu,production \
  --work /custom/work/directory \
  --runnergroup Production \
  --replace
```

## Command Line Options

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `--url` | Yes | Repository or organization URL | - |
| `--token` | Yes | Runner registration token from GitHub | - |
| `--name` | No | Custom name for the runner | System hostname |
| `--work` | No | Working directory for runner jobs | `_work` |
| `--labels` | No | Comma-separated custom labels | `self-hosted,<os>,<arch>` |
| `--runnergroup` | No | Runner group name | `Default` |
| `--replace` | No | Replace existing runner with same name | Not set |
| `--unattended` | No | Run in unattended mode | `true` |
| `--help` | No | Show help message | - |

## What the Script Does

1. **Detects System**: Automatically identifies OS (Linux/macOS) and architecture (x64/ARM64/ARM)
2. **Downloads Latest Runner**: Fetches the most recent GitHub Actions runner release
3. **Extracts Package**: Unpacks the runner to `~/actions-runner` directory
4. **Configures Runner**: Sets up the runner with your provided token and settings
5. **Installs Service**:
   - Linux: Creates and starts a systemd service
   - macOS: Creates and starts a launchd service
6. **Starts Runner**: Automatically starts the runner to accept jobs

## Installation Directory

By default, the runner is installed in:
```
~/actions-runner/
```

This directory contains:
- Runner binaries and scripts
- Configuration files
- Work directory (where jobs execute)
- Log files

## Managing the Runner Service

### Linux (systemd)

```bash
cd ~/actions-runner

# Check status
sudo ./svc.sh status

# Stop the runner
sudo ./svc.sh stop

# Start the runner
sudo ./svc.sh start

# Uninstall the service
sudo ./svc.sh uninstall
```

### macOS (launchd)

```bash
cd ~/actions-runner

# Check status
./svc.sh status

# Stop the runner
./svc.sh stop

# Start the runner
./svc.sh start

# Uninstall the service
./svc.sh uninstall
```

## Uninstalling the Runner

To completely remove the runner:

### Linux

```bash
cd ~/actions-runner
sudo ./svc.sh stop
sudo ./svc.sh uninstall
./config.sh remove --token YOUR_REMOVAL_TOKEN
cd ~
rm -rf ~/actions-runner
```

### macOS

```bash
cd ~/actions-runner
./svc.sh stop
./svc.sh uninstall
./config.sh remove --token YOUR_REMOVAL_TOKEN
cd ~
rm -rf ~/actions-runner
```

**Note**: You'll need a new token for removal. Generate it the same way as the registration token.

## Examples

### Repository Runner with Custom Name

```bash
./install-github-runner.sh \
  --url https://github.com/mycompany/myapp \
  --token AX7EXAMPLE2TOKEN3HERE4567 \
  --name production-runner-01
```

### Organization Runner with Custom Labels

```bash
./install-github-runner.sh \
  --url https://github.com/mycompany \
  --token AX7EXAMPLE2TOKEN3HERE4567 \
  --labels self-hosted,linux,docker,kubernetes \
  --runnergroup Production
```

### Replace Existing Runner

```bash
./install-github-runner.sh \
  --url https://github.com/mycompany/myapp \
  --token AX7EXAMPLE2TOKEN3HERE4567 \
  --name my-runner \
  --replace
```

## Troubleshooting

### Runner Not Starting

1. Check if the service is running:
   ```bash
   cd ~/actions-runner
   # Linux
   sudo ./svc.sh status
   # macOS
   ./svc.sh status
   ```

2. Check runner logs:
   ```bash
   cd ~/actions-runner
   tail -f _diag/*.log
   ```

### Token Expired

If you see authentication errors, your token may have expired. Generate a new token and run the script again with the `--replace` flag.

### Permission Denied

- On Linux, service installation requires sudo
- Ensure the script is executable: `chmod +x install-github-runner.sh`
- Check that you have write permissions to `~/actions-runner`

### Architecture Not Supported

The script supports:
- x64 (x86_64)
- ARM64 (aarch64, arm64)
- ARM (armv7l)

If your architecture isn't supported, you'll see an error message during detection.

### Service Installation Failed

If service installation fails, the runner will start in background mode. You can:
- Run manually: `cd ~/actions-runner && ./run.sh`
- Check system logs for service errors
- Ensure systemd (Linux) or launchd (macOS) is available

## Security Considerations

1. **Token Security**: Never commit runner tokens to version control
2. **Runner Isolation**: Consider running runners in isolated environments (VMs, containers)
3. **Network Security**: Ensure runners can only access necessary resources
4. **Updates**: Regularly check for runner updates through GitHub
5. **User Permissions**: Run the service with minimal required permissions

## Supported Platforms

### Linux
- Ubuntu 20.04+
- Debian 10+
- CentOS 8+
- RHEL 8+
- Fedora (recent versions)
- Other systemd-based distributions

### macOS
- macOS 11 (Big Sur) or later
- Intel and Apple Silicon (M1/M2) Macs

## Additional Resources

- [GitHub Actions Self-Hosted Runners Documentation](https://docs.github.com/en/actions/hosting-your-own-runners)
- [About Self-Hosted Runners](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners)
- [Runner Releases](https://github.com/actions/runner/releases)