# 🗺️ Project Roadmap: MTG Card Manager for Obsidian

This roadmap outlines the planned development path for the MTG Card Manager. Items are subject to change based on project needs and my current learnings.

## ✅ Completed Features (Current Version)

- **Card Creation**: Scrape Scryfall URLs to create Obsidian markdown files with images, metadata, and tags.
- **Card Deletion**: Remove card files and their associated images safely.
- **Image Cleanup**: Automatic removal of unused image files from the local directory.
- **Grouping Tags**: CRUD operations for custom grouping tags.
- **Data Persistence**: Automated management of collection lists, card types, and groups.
- **Modern Python Architecture**: Partial refactor using `Pathlib`, `Dataclasses`, and `Type Hints`.
- **Robust Error Handling**: Friendly error messages for network and API failures.

---

## 🚀 Planned Phases

### Phase 1: Menu Refactoring & UX (Short-term)
*Goal: Improve the CLI organization and user experience.*

- [x] **Submenu: Utilities**
  - [x] Move "Remove unused images" to Utilities.
  - [x] Add tool to view/edit collection list (`collections.md`).
  - [x] Add tool to recreate collection list from existing card files.
  - [x] Add tool to view/edit type list (`types.md`).
- [x] **Submenu: Card Management**
  - [x] Move "Add card" and "Find and delete" to Card Management.
  - [x] Implement card editing (update metadata/notes without re-adding).
- [x] **Unified UI Components**: Standardize prompts and error handling across all modules.

### Phase 2: Enhanced Card Operations (Mid-term)
*Goal: Expand how cards can be added and manipulated.*

- [ ] **Advanced Search & Select**
  - [ ] Search cards by name via Scryfall API without requiring a URL.
  - [ ] Select from multiple results if multiple prints exist.
- [ ] **Batch Operations**
  - [ ] Update metadata for multiple cards at once (e.g., change grouping for a selection).
  - [ ] Create multiple cards from a list of URLs or names.
- [ ] **Deck/List Import**: Import cards from a text-based list (CSV or MTGO format).

### Phase 3: Base & Config Management (Long-term)
*Goal: Support multiple Obsidian vaults and flexible configurations.*

- [ ] **Multi-Base Support**
  - [ ] Initialize a new Obsidian vault structure for MTG.
  - [ ] Switch between different vaults/config profiles.
- [ ] **Improved Configuration**
  - [ ] Move configuration to a more robust format (YAML or JSON).
  - [ ] Dynamic path configuration for images and card files.
- [ ] **Stats Dashboard**: CLI-based summary of the collection (total cards, distribution by type/color).

### Phase 4: Modern Interface (Future)
*Goal: Transcend the CLI for better accessibility.*

- [ ] **Graphical User Interface (GUI)**
  - [ ] Explore frameworks (e.g., CustomTkinter, PySide, or a web-based local UI).
  - [ ] Visual card gallery view.
- [ ] **Obsidian Plugin (Optional)**: Explore porting logic to a native Obsidian plugin (TypeScript).

---

## 🛠️ Internal Maintenance
- [ ] Add unit tests for core logic (`card_manager.py`, `scryfall.py`).
- [ ] Improve error logging.
- [x] Refactor `main.py` to be more modular as menus expand.
