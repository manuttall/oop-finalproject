# Python Rendering Engine Project

A project designed to emphasize object-oriented programming strategies in building a 3D rendering engine.

| Name | Python Rendering Engine |
| :--- | :--- |
| Description | A 3D rendering engine project designed to emphasize object oriented programming coding strategies. |
| Due Date | 8-May-2025 |
| Status | Complete |
| Location | https://github.com/manuttall/oop-finalproject/tree/main/renderer|
| Self Grade | 100/100 |
| Notes | 1st place project for CMU Student Showcase 2025. |

## 📝 Justification for Self-Grade

This project exhibits a high level of technical sophistication in both implementation and design. Advanced mathematical reasoning, custom algorithms, and heuristics were developed to construct the 3D rendering engine while hiding this complexity behind abstraction and an intuitive interface to prioritize user experience. 

More than three design patterns are used, including Singleton, Builder, Adapter, Template, and Composite. Fundamental object-oriented design principles such as inheritance, abstraction, encapsulation (getters/setters), and class-based modeling are thoroughly applied.

We managed the project using GitHub Issues and a Kanban board via GitHub Projects. The entire codebase is well-documented using `pdoc`. We implemented the 4+1 architectural view model and extended it to include scenario, logical, developer, process, physical, and context views with UML diagrams.

Testing is comprehensive: over 15 test modules with nearly 200 test functions, utilizing hypothesis, mocking, patching, CI/CD pipelines, Docker integration, and type checking. Tests were authored by teammates for each other’s modules, ensuring independent coverage. The codebase is cleanly separated into logical packages and modules, with clear class responsibilities. Every team member contributed fully across all levels of development.

---

## 📁 File Structure

```
📁 renderer/ - Main folder containing the project and engine
├── engine.py         - Main engine used to run the program
├── Makefile          - Used to test or run the Render engine 
├── 📁 assets/         - Contains .obj files to be rendered
├── 📁 docs/
│   ├── 📁 code-docs/  - Documentation generated via pdocs
│   ├── 📁 pycov/      - Testing coverage documentation
├── 📁 geometry/       - Geometric data classes
├── 📁 scene/          - Scene data and math utility classes
├── 📁 tests/          - All unit testing code
├── 📁 uml/            - UML diagrams of the system
├── 📁 utility/        - File and data management utilities
```

---

## 🧪 How to Test

To run all unit tests:

1. From the root `oop-finalproject` directory, run the Docker container:
   ```bash
   bash run-docker.sh
   ```

2. Inside the container, navigate into the renderer project:
   ```bash
   cd renderer
   ```

3. Run all tests using `make`:
   ```bash
   make all
   ```

This will run the full suite of unit tests and output coverage reports.

---

## 🚀 How to Run

> ⚠️ Ensure you are **not** running inside a container or remote environment. This application is meant to run in your **native local environment**.

1. Navigate into the `renderer` folder:
   ```bash
   cd renderer
   ```

2. Launch the rendering engine using:
   ```bash
   make run
   ```
   This will open the default graphical interface:  
   ![Interface Default](https://github.com/manuttall/oop-finalproject/blob/main/screenshots/program_interface_default.png)

3. Inside the interface, input values such as:
   - **Filename**: Name of an `.obj` file in the `assets` folder
   - **Camera Position (x y z)**: e.g., `3 3 3`
   - **Look-at Position (x y z)**: e.g., `0 0 0`
   - **Camera Aspect Ratio (H V)**: e.g., `4 3`
   - **Resolution**: e.g., `512`
   - **Background Color (R G B)**: e.g., `255 255 255`
   - **Color Variance (int ≥ 0)**: e.g., `10`

   Example setup:  
   ![Interface Configured](https://github.com/manuttall/oop-finalproject/blob/main/screenshots/program_interface_set.png)

4. Press **Render**. The engine will load the 3D model and display the rendered result:
   ![Rendered Bonsai](https://github.com/manuttall/oop-finalproject/blob/main/screenshots/program_bonsai.png)

---

### 🎨 Color Variance Explanation

The **color variance** setting adds slight randomized variance to the base colors of surfaces. This mimics lighting variation and brings additional depth and form to otherwise flat 3D models.

Example with variance enabled:
![Shader Variance](https://github.com/manuttall/oop-finalproject/blob/main/screenshots/program_shader_variance.png)

---

## 🧱 Design Patterns Used

- **Singleton**: Used in the `Engine` manager class to ensure only one engine instance is active at a time. Also applied in `FileImport` to manage shared import behavior across multiple files.

- **Builder**: The `FileImport` class constructs complex `Mesh` objects by incrementally adding `Face3D` instances and then applying a `Shader`.

- **Adapter**: The `Camera` class acts as an adapter by transforming `Face3D` objects (3D geometry) into `Face2D` projections suitable for 2D rendering.

- **Template**: `Coordinate3D` is an abstract base class (template) for both `Vertex` and `Vector`, encapsulating shared behavior in 3D space.

- **Composite**: Nearly all classes (e.g., `Scene`, `Mesh`, `Face3D`, `Camera`) are composed of smaller objects, except for utility data classes like `Point`, `Coord3D`, `Shader`, `AspectRatio`, and `Interface`.
