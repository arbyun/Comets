# Comets 🚀  

A simple arcade-style space shooter built with Pygame. Dodge and destroy incoming comets while managing your score to purchase upgrades!  

## ℹ️ About  

**Comets** is a fast-paced arcade shooter where players control a spaceship, dodging and destroying incoming comets. With each comet destroyed, the difficulty increases, pushing players to react quickly and strategize their shots.  

Players can spend their score in the **Upgrade Shop**, where they can trade points for power-ups—but at the cost of lowering their high score. Can you survive the meteor storm and climb the leaderboard?  

---

## 📌 About the Project  

This game was developed by:  
- **Daniela Dantas (22202104)** – UI design, leaderboard, and main game integration.  
- **Vitória Rodrigues (22204356)** – Initial prototype, movement mechanics, and comet drawing.  

The project is structured as follows:  
- **Main Menu**: Handles the game’s starting interface.  
- **Game Loop**: Manages player controls, difficulty scaling, collision detection, and drawing elements.  
- **Leaderboards**: Stores and displays high scores.  
- **Game Over Screen**: Displays results after a game session.  
- **Gameplay Features**: Includes sound effects, player mechanics, projectile handling, and enemy comets.  

External libraries used: `time`, `math`, and `random`.  

---

## 🎮 Controls  

- **Move the spaceship** – Arrow keys  
- **Shoot projectiles** – Spacebar  
- **Pause the game** – P  
- **Access the upgrade shop** – Press P (in pause menu), navigate with ↑ / ↓, and confirm with Enter  

---

## 🛒 Upgrade Shop  

Players can spend their score to purchase upgrades, but be mindful—each upgrade requires sacrificing a portion of your points!  

---

## 🛠️ Instructions 

To run **Comets**, follow these steps:  

1. **Clone the repository**  
   ```sh
   git clone https://github.com/arbyun/Comets.git
   cd comets
   ```
   
2. **Install dependencies (requires Python and Pygame)**
   ```sh
   pip install pygame
   ```
3. **Run the game**
   ```sh
   python main.py
   ```

## 📜 License  

This project is licensed under the **MIT License**.  See the [LICENSE](LICENSE) file for more details.  
