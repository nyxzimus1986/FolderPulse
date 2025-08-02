<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# FolderPulse Copilot Instructions

## Project Overview
FolderPulse is a comprehensive Python application for file system monitoring and management with both GUI and web dashboard capabilities. The application is built with a modular architecture using modern Python practices.

## Architecture Guidelines
- **MVC Pattern**: Follow Model-View-Controller pattern with clear separation of concerns
- **Modular Design**: Keep components loosely coupled and highly cohesive
- **Error Handling**: Always include proper exception handling and logging
- **Type Hints**: Use type hints for better code clarity and IDE support

## Code Style Preferences
- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Add docstrings for all classes and functions
- Include type hints for function parameters and return values
- Keep functions focused and small (ideally under 50 lines)

## Project Structure
```
src/
├── main.py              # Application entry point
├── core/                # Core business logic
│   └── app_manager.py   # Central application manager
├── gui/                 # GUI components
│   └── main_window.py   # Main Tkinter interface
└── utils/               # Utility modules
    └── logger.py        # Logging utilities
```

## Key Technologies
- **GUI**: Tkinter for desktop interface
- **Web**: Flask + SocketIO for web dashboard
- **Monitoring**: Watchdog for file system events
- **Configuration**: JSON-based configuration management
- **Logging**: Python logging with rotation
- **Building**: PyInstaller for executable creation

## Development Practices
- Use the existing logger from `utils.logger` for all logging
- Follow the configuration pattern established in `core.app_manager`
- Maintain the GUI structure established in `gui.main_window`
- Add proper error handling and user feedback
- Write unit tests for new functionality

## Common Patterns
- Use `self.logger = logging.getLogger(__name__)` in classes
- Access configuration via `self.app_manager.get_config(key, default)`
- Handle GUI events with proper error handling and user feedback
- Use pathlib.Path for file system operations
- Implement cleanup methods for resource management

## Testing Guidelines
- Write tests for all new functionality
- Use pytest for testing framework
- Mock external dependencies
- Test both success and failure scenarios
- Include integration tests for GUI components

## When Adding New Features
1. Consider impact on existing architecture
2. Add appropriate logging and error handling
3. Update configuration schema if needed
4. Create or update tests
5. Update documentation as needed
