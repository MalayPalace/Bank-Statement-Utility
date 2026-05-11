# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v2.1.2] - May 11, 2026

### Added
- Hdfc Credit Card statement processor
- Yes Bank Credit card statement processor
- Manual Entry screen with Validation
- Statistics View to show last updated date and closing balance
- Guide screen to show supported formats
- Export as Type QIF
- Xlsx parser

### Changed
- Kotak Credit card as per new pdf format
- Show Hint in verification when failed
- Config writer to update only once between version

## [v2.0.0] - Jun 14, 2024

### Added
- UI module in front of the backend CLI commands.
- Tkinter ttk based UI wrapped with ttkbootstrap theme
- Integration of Process/Verify/Export with the UI

### Changed
- Config path changed for Windows
- Config writer updated to handle version update

## [v1.2.1] - Jan 16, 2024

### Added
- Credit Card Statements Reader for Kotak and SBI Banks
- PdfParser added to read PDF statements
- ConfigWriter to write default config.ini file without needing manual copying

## [v1.1.0] - Aug 25, 2023

### Added
- Initial release
