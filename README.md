# PhyPy

# AIM (Augmented Reality Integration for Modern Learning)

AIM transforms any laptop or webcam-equipped device into an interactive portal for dynamic physics lessons. By capturing hand gestures through a standard webcam, AIM drives a 2D physics simulation on screen—illustrating gravity, elasticity, and directional wind forces in real time. Delivered as a free, software-only solution, AIM removes reliance on specialized AR hardware, broadening access to immersive STEM education.

---

## Installation

Make sure you have Python 3.11 installed, then run:

```bash
pip install -r requirements.txt
```

Adjust window size to your liking @ app.py
```python
#(width, height)
App((900, 1000)).run()
```

---

## Project Background

### 1.1 Background and Context

AIM is grounded in constructivism and experiential learning theories, which hold that learners build deeper understanding through active engagement. By translating real-world hand gestures into simulation inputs, AIM bridges abstract physics concepts with tangible interaction.

Many existing immersive learning tools demand costly AR hardware—out of reach for underfunded schools or remote regions. AIM addresses this gap by using ubiquitous webcams and a lightweight 2D engine to deliver compelling physics demonstrations.

### 1.2 Statement of the Problem

#### 1.2.1 Main Problem

Many educational settings lack affordable, hands-on tools to vividly demonstrate abstract physics concepts.

#### 1.2.2 Sub-Problems

- Accessibility: Specialized AR gear is expensive and logistically challenging.
- Engagement: Traditional lectures and static diagrams fail to bring forces and motion to life.
- Interactivity: Most simulations do not adapt in real time to user inputs, limiting experiential feedback.

#### 1.2.3 Primary Beneficiaries

- Educators: Gain a cost-effective tool for enriching lesson plans and driving student interest.
- Students: Especially in underserved areas, benefit from hands-on simulations that improve concept retention.
- Educational Institutions: Integrate AIM into STEM curricula without investing in expensive hardware, paving the way for more inclusive and modern educational practices.

---

## Features

- Real-time hand-gesture capture via webcam  
- Simple 2D physics engine modeling gravity, elasticity, and wind (horizontal & vertical)  
- Cross-platform support on any Python 3.11 environment  
- Zero additional hardware required  

---

## Usage

1. Install dependencies (`pip install -r requirements.txt`).  
2. Connect a webcam to your laptop or desktop.  
3. Launch the simulation:

    ```bash
    python3.11 app.py
    ```

4. Use hand gestures to interact with the on-screen ball and observe how various forces affect its motion.

---

## Future Enhancements

- AI-driven guidance to scaffold student learning  
- Advanced gesture calibration for more precise control  
- Expanded physics models (e.g., rotational dynamics, collisions among multiple objects)  
- Web-based deployment for global classroom integration  

---

## License

This project is released under the MIT License. Feel free to use, modify, and distribute as long as the original copyright and license notice are included.
