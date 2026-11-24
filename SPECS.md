# Project Specification: Dimensional Rift - A Choose Your Own Adventure Game

## 1. Project Overview

**Title:** (Working Title) Dimensional Rift: The Living Sunstone

**Platform:** Command Line / Terminal
**Language:** Python 3.x
**Genre:** Text-based "Choose Your Own Adventure" (CYOA) RPG
**Core Concept:** A 10-stage interactive fiction game where the player navigates a branching storyline based on a specific narrative universe. Every interaction presents exactly 3 choices, leading to diverging paths, overlapping events, and ultimately, distinct endings based on the accumulated decisions.

## 2. Core Gameplay Mechanics

### 2.1 The 10-Interaction Structure

* The game consists of exactly **10 decision points (interactions)** per playthrough.

* At each interaction, the player reads a segment of the story and is presented with exactly **3 distinct choices**.

* Choosing an option resolves the current scenario, reveals the immediate consequences, and pushes the player to the next node, increasing the turn counter by 1.

* After the 10th choice is made, the game calculates and displays a specific ending based on the path taken, then returns to the main menu.

### 2.2 Branching and Overlapping Paths

* **Branching:** Choices lead to different "Nodes" (story states).

* **Overlapping:** To manage complexity, branches can converge. A choice presented in Node A might lead to the same subsequent Node as a choice in Node B. Previously unselected choices can reappear in future nodes if they remain relevant to the story state.

## 3. User Interface & Menus

### 3.1 Main Menu

When the script is executed, the console will clear and display the title and a Main Menu with three options:

1. **Start New Game:** Clears any existing save data, resets the turn counter to 0, and loads the introductory story node.

2. **Continue:** Loads the player's saved state (current node and turn counter) from a local file (e.g., `savegame.json`). If no save exists, notifies the user and returns to the menu.

3. **Quit:** Exits the Python application.

### 3.2 In-Game Interface

For every turn, the terminal will display:

1. **Turn Counter:** (e.g., `[Interaction 3/10]`)

2. **Story Text:** A descriptive paragraph of the current events.

3. **Options:**

   * `1. [Choice A text]`

   * `2. [Choice B text]`

   * `3. [Choice C text]`

4. **Input Prompt:** `What will you do? (1/2/3): `

*Input validation must be implemented to handle typos or invalid numbers gracefully, prompting the user until a valid choice (1, 2, or 3) is entered.*

## 4. Technical Architecture

### 4.1 Data Structure (JSON)

The story nodes should be stored in a `.json` file or Python dictionary to keep the logic separate from the content.
**Example Node Schema:**

```
{
  "node_id": "start_01",
  "text": "Bob, a TDS scientist, finds himself stranded in an alternate dimension after using a prototype Jump Portal...",
  "choices": [
    {
      "text": "Search for indigenous materials to build a new portal.",
      "next_node": "node_02a"
    },
    {
      "text": "Approach the man with the robotic arm in the distance.",
      "next_node": "node_02b"
    },
    {
      "text": "Consult your AI earpiece for an environmental scan.",
      "next_node": "node_02c"
    }
  ]
}

```

### 4.2 Save/Load System

* The game will automatically save progress at the start of each new node.

* State is saved to `save.json` containing: `{"current_node": "node_05c", "turn_count": 5}`.

## 5. Narrative Framework & Lore Guide

The AI or writer generating the node content must adhere to the following lore and character details:

### 5.1 Characters

* **Bob:** Scientist for TDS (Transdimensional Solutions) under PRAP (Parallel Reality Portal Access). Stuck in an alternate dimension. Relies on an intelligent AI earpiece (borrowed from Matteo) to understand the world.

* **Matteo:** A local with a robotic arm capable of shape-shifting via microchips. Former member of an assassination/mercenary group called Vylopoth.

* **Creature:** A dragon whose parents were killed by the Sunstone. Holds a grudge against Matteo for triggering the stone.

* **The Mummy:** An ancient being found in the Honapopary training grounds. Holds valuable information about the world's relics (including the Sunstone).

* **Vylopoth:** A ruthless organization hunting Matteo for defecting.

### 5.2 Key Plot Points (To be woven into the branches)

* **The Tuum Expedition:** Bob and Matteo travel to Tuum to find the Sunstone, a massive power source Bob needs for his Jump Portal.

* **The Sunstone Corruption:** Matteo embeds the Sunstone into his robotic arm. The AI warns Bob it is evil. Matteo becomes aggressive. In the night, the stone acts on its own, destroying trees.

* **The Betrayal:** Bob violently tears the stone from sleeping Matteo's arm to save him from complete corruption and flees. Matteo wakes up injured (lacking life force), finds Bob gone, and assumes Bob betrayed him.

* **The Reunion at Honapopary:** Matteo (now traveling with Creature) searches for Bob and finds him in the floating island arena of Honapopary fighting a Mummy. Matteo saves Bob.

* **The Truce:** Bob explains his actions. Creature tries to kill Matteo out of revenge for the Sunstone. Matteo tranqs the Mummy to stop an ultimate attack. They escape together to hide from Vylopoth and extract relic info from the captured Mummy.

### 5.3 Ending Conditions (Turn 10)

Endings will be determined by the final node reached on Turn 10. Examples of potential endings based on the story:

* **Good Ending:** Bob gathers the materials and info from the Mummy, successfully building the Jump Portal while Matteo and Creature fend off Vylopoth.

* **Tragic Ending:** The Sunstone reclaims Matteo, or Vylopoth catches up to the group before the portal can be built.

* **Neutral/Cliffhanger Ending:** Bob successfully escapes through the portal, but Matteo and Creature are left behind to face Vylopoth, forever changing their world.