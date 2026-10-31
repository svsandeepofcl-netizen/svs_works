#!/usr/bin/env python3
"""
Jungle Viper - Native Python Desktop Game (Tkinter)
Runs with zero external pip dependencies.
Features:
- Arrow keys controls (Up, Down, Left, Right)
- Realistic green snake with head, eyes, and size growth
- Self-collision and perimeter collision detection
- Persistent Top 5 Leaderboard saved in scores.json
"""

import json
import math
import os
import random
import sys
import tkinter as tk
from typing import List, Tuple

GAME_DIR = os.path.dirname(os.path.abspath(__file__))
SCORES_FILE = os.path.join(GAME_DIR, "scores.json")

CELL_SIZE = 22
GRID_COLS = 28
GRID_ROWS = 28
CANVAS_WIDTH = CELL_SIZE * GRID_COLS
CANVAS_HEIGHT = CELL_SIZE * GRID_ROWS
GAME_SPEED_MS = 135


def load_top_scores() -> List[dict]:
    default_scores = [
        {"name": "Anaconda King", "score": 250},
        {"name": "Green Mamba", "score": 180},
        {"name": "Emerald Viper", "score": 120},
        {"name": "Cobra Scout", "score": 70},
        {"name": "Jungle Novice", "score": 30},
    ]
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    return sorted(data, key=lambda x: x["score"], reverse=True)[:5]
        except Exception:
            pass
    return default_scores


def save_top_scores(scores: List[dict]) -> None:
    try:
        sorted_scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:5]
        with open(SCORES_FILE, "w", encoding="utf-8") as f:
            json.dump(sorted_scores, f, indent=2)
    except Exception as e:
        print(f"[!] Could not save scores: {e}", file=sys.stderr)


class JungleViperApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Jungle Viper - Realistic Snake Hunt")
        self.root.resizable(False, False)
        self.root.configure(bg="#07130a")

        self.snake: List[Tuple[int, int]] = []
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food = (10, 10)
        self.score = 0
        self.is_running = False
        self.is_paused = False
        self.tongue_toggle = False
        self.top_scores = load_top_scores()

        self.setup_ui()
        self.bind_keys()
        self.start_game()

    def setup_ui(self):
        # Header Stats
        header_frame = tk.Frame(self.root, bg="#0e1d12", padx=16, pady=10)
        header_frame.pack(fill=tk.X)

        title_lbl = tk.Label(
            header_frame,
            text="🌿 JUNGLE VIPER",
            font=("Segoe UI", 16, "bold"),
            fg="#34d399",
            bg="#0e1d12",
        )
        title_lbl.pack(side=tk.LEFT)

        self.top_score_lbl = tk.Label(
            header_frame,
            text=f"TOP: {self.top_scores[0]['score']}",
            font=("Segoe UI", 11, "bold"),
            fg="#f59e0b",
            bg="#0e1d12",
            padx=14,
        )
        self.top_score_lbl.pack(side=tk.RIGHT)

        self.score_lbl = tk.Label(
            header_frame,
            text="SCORE: 0  |  LENGTH: 3",
            font=("Segoe UI", 12, "bold"),
            fg="#f0fdf4",
            bg="#0e1d12",
        )
        self.score_lbl.pack(side=tk.RIGHT)

        # Main Layout: Game Canvas + Leaderboard Sidebar
        main_frame = tk.Frame(self.root, bg="#07130a", padx=12, pady=12)
        main_frame.pack()

        # Canvas
        self.canvas = tk.Canvas(
            main_frame,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg="#0a1f11",
            highlightthickness=2,
            highlightbackground="#22c55e",
        )
        self.canvas.pack(side=tk.LEFT, padx=6)

        # Leaderboard Sidebar
        side_frame = tk.Frame(main_frame, bg="#0e1d12", padx=14, pady=14, width=220)
        side_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=6)
        side_frame.pack_propagate(False)

        lead_title = tk.Label(
            side_frame,
            text="🏆 TOP 5 HUNTERS",
            font=("Segoe UI", 12, "bold"),
            fg="#fef08a",
            bg="#0e1d12",
        )
        lead_title.pack(anchor="w", pady=(0, 10))

        self.leader_labels = []
        for i in range(5):
            lbl = tk.Label(
                side_frame,
                text="",
                font=("Segoe UI", 10),
                fg="#a7f3d0",
                bg="#0e1d12",
                anchor="w",
            )
            lbl.pack(fill=tk.X, pady=3)
            self.leader_labels.append(lbl)

        self.refresh_leaderboard_ui()

        # Controls instructions
        ctrl_title = tk.Label(
            side_frame,
            text="\n🎮 CONTROLS",
            font=("Segoe UI", 10, "bold"),
            fg="#86efac",
            bg="#0e1d12",
        )
        ctrl_title.pack(anchor="w")

        controls_text = (
            "• ▲ / W : Up\n"
            "• ▼ / S : Down\n"
            "• ◄ / A : Left\n"
            "• ► / D : Right\n"
            "• Space : Pause\n"
            "• R     : Restart"
        )
        ctrl_lbl = tk.Label(
            side_frame,
            text=controls_text,
            font=("Segoe UI", 9),
            fg="#6ee7b7",
            bg="#0e1d12",
            justify=tk.LEFT,
        )
        ctrl_lbl.pack(anchor="w", pady=4)

    def bind_keys(self):
        self.root.bind("<Up>", lambda e: self.change_dir(0, -1))
        self.root.bind("<Down>", lambda e: self.change_dir(0, 1))
        self.root.bind("<Left>", lambda e: self.change_dir(-1, 0))
        self.root.bind("<Right>", lambda e: self.change_dir(1, 0))

        self.root.bind("<w>", lambda e: self.change_dir(0, -1))
        self.root.bind("<s>", lambda e: self.change_dir(0, 1))
        self.root.bind("<a>", lambda e: self.change_dir(-1, 0))
        self.root.bind("<d>", lambda e: self.change_dir(1, 0))

        self.root.bind("<space>", lambda e: self.toggle_pause())
        self.root.bind("<r>", lambda e: self.start_game())

    def change_dir(self, dx: int, dy: int):
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.next_direction = (dx, dy)

    def toggle_pause(self):
        if not self.is_running:
            return
        self.is_paused = not self.is_paused
        if not self.is_paused:
            self.game_step()

    def start_game(self):
        self.snake = [(10, 14), (9, 14), (8, 14)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.is_running = True
        self.is_paused = False
        self.spawn_food()
        self.update_score_ui()
        self.game_step()

    def spawn_food(self):
        while True:
            fx = random.randint(1, GRID_COLS - 2)
            fy = random.randint(1, GRID_ROWS - 2)
            if (fx, fy) not in self.snake:
                self.food = (fx, fy)
                break

    def update_score_ui(self):
        self.score_lbl.config(text=f"SCORE: {self.score}  |  LENGTH: {len(self.snake)}")
        self.top_score_lbl.config(text=f"TOP: {self.top_scores[0]['score']}")

    def refresh_leaderboard_ui(self):
        medals = ["🥇", "🥈", "🥉", "4.", "5."]
        for i, item in enumerate(self.top_scores[:5]):
            self.leader_labels[i].config(
                text=f"{medals[i]} {item['name'][:12]}: {item['score']} pts"
            )

    def game_step(self):
        if not self.is_running or self.is_paused:
            return

        self.direction = self.next_direction
        head_x = self.snake[0][0] + self.direction[0]
        head_y = self.snake[0][1] + self.direction[1]

        # 1. Boundary / Wall check
        if head_x < 0 or head_x >= GRID_COLS or head_y < 0 or head_y >= GRID_ROWS:
            self.game_over("The viper crashed into jungle border vines!")
            return

        # 2. Self-collision: Touching its own body
        if (head_x, head_y) in self.snake:
            self.game_over("The viper bit its own body! Self-cannibalism is fatal.")
            return

        # Add new head
        self.snake.insert(0, (head_x, head_y))

        # Check food consumption
        if (head_x, head_y) == self.food:
            self.score += 10
            self.update_score_ui()
            self.spawn_food()
            # Note: Snake size increases because tail is not removed!
        else:
            self.snake.pop()

        self.tongue_toggle = not self.tongue_toggle
        self.draw()

        self.root.after(GAME_SPEED_MS, self.game_step)

    def game_over(self, reason: str):
        self.is_running = False

        # Check Top 5 Score
        is_high = self.score > 0 and (
            len(self.top_scores) < 5 or self.score > self.top_scores[-1]["score"]
        )
        if is_high:
            self.top_scores.append({"name": "Player 1", "score": self.score})
            save_top_scores(self.top_scores)
            self.top_scores = load_top_scores()
            self.refresh_leaderboard_ui()

        # Draw game over overlay
        self.canvas.create_rectangle(
            40,
            CANVAS_HEIGHT // 2 - 90,
            CANVAS_WIDTH - 40,
            CANVAS_HEIGHT // 2 + 90,
            fill="#051208",
            outline="#ef4444",
            width=2,
        )
        self.canvas.create_text(
            CANVAS_WIDTH // 2,
            CANVAS_HEIGHT // 2 - 50,
            text="💀 SNAKE PERISHED!",
            font=("Segoe UI", 18, "bold"),
            fill="#fca5a5",
        )
        self.canvas.create_text(
            CANVAS_WIDTH // 2,
            CANVAS_HEIGHT // 2 - 15,
            text=reason,
            font=("Segoe UI", 10),
            fill="#fecaca",
        )
        self.canvas.create_text(
            CANVAS_WIDTH // 2,
            CANVAS_HEIGHT // 2 + 20,
            text=f"Final Score: {self.score}",
            font=("Segoe UI", 14, "bold"),
            fill="#f59e0b",
        )
        self.canvas.create_text(
            CANVAS_WIDTH // 2,
            CANVAS_HEIGHT // 2 + 55,
            text="Press 'R' to Play Again",
            font=("Segoe UI", 10, "italic"),
            fill="#a7f3d0",
        )

    def draw(self):
        self.canvas.delete("all")

        # Jungle Grid Vines
        for c in range(GRID_COLS):
            x = c * CELL_SIZE
            self.canvas.create_line(x, 0, x, CANVAS_HEIGHT, fill="#0d2916", width=1)
        for r in range(GRID_ROWS):
            y = r * CELL_SIZE
            self.canvas.create_line(0, y, CANVAS_WIDTH, y, fill="#0d2916", width=1)

        # Draw Food (Golden / Ruby Jungle Berry)
        fx = self.food[0] * CELL_SIZE
        fy = self.food[1] * CELL_SIZE
        self.canvas.create_oval(
            fx + 2, fy + 2, fx + CELL_SIZE - 2, fy + CELL_SIZE - 2,
            fill="#ef4444", outline="#fca5a5", width=2
        )
        self.canvas.create_oval(
            fx + 5, fy + 5, fx + 9, fy + 9, fill="#ffffff", outline=""
        )

        # Draw Snake (Realistic Green Viper Shades)
        # Body segments
        for i in range(len(self.snake) - 1, 0, -1):
            seg = self.snake[i]
            sx = seg[0] * CELL_SIZE
            sy = seg[1] * CELL_SIZE

            # Color gradient: head is lighter emerald, tail is deeper forest green
            ratio = i / len(self.snake)
            if ratio < 0.35:
                color = "#10b981"  # Emerald
            elif ratio < 0.7:
                color = "#059669"  # Rainforest
            else:
                color = "#047857"  # Deep Forest

            self.canvas.create_oval(
                sx + 1, sy + 1, sx + CELL_SIZE - 1, sy + CELL_SIZE - 1,
                fill=color, outline="#022c22", width=1
            )
            # Dorsal spine scale dot
            self.canvas.create_oval(
                sx + CELL_SIZE // 2 - 2, sy + CELL_SIZE // 2 - 2,
                sx + CELL_SIZE // 2 + 2, sy + CELL_SIZE // 2 + 2,
                fill="#fde047", outline=""
            )

        # Head (Snake[0])
        head = self.snake[0]
        hx = head[0] * CELL_SIZE
        hy = head[1] * CELL_SIZE
        self.canvas.create_oval(
            hx, hy, hx + CELL_SIZE, hy + CELL_SIZE,
            fill="#34d399", outline="#065f46", width=2
        )

        # Eyes & Tongue based on direction
        dx, dy = self.direction
        cx = hx + CELL_SIZE // 2
        cy = hy + CELL_SIZE // 2

        # Eyes
        if dx != 0:
            eye1 = (cx + dx * 4, cy - 5)
            eye2 = (cx + dx * 4, cy + 5)
        else:
            eye1 = (cx - 5, cy + dy * 4)
            eye2 = (cx + 5, cy + dy * 4)

        for ex, ey in (eye1, eye2):
            self.canvas.create_oval(ex - 2, ey - 2, ex + 2, ey + 2, fill="#f59e0b", outline="")
            self.canvas.create_oval(ex - 1, ey - 1, ex + 1, ey + 1, fill="#000000", outline="")

        # Flickering Red Tongue
        if self.tongue_toggle:
            tx = cx + dx * (CELL_SIZE // 2 + 4)
            ty = cy + dy * (CELL_SIZE // 2 + 4)
            self.canvas.create_line(cx + dx * 6, cy + dy * 6, tx, ty, fill="#ef4444", width=2)


def main():
    root = tk.Tk()
    app = JungleViperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
