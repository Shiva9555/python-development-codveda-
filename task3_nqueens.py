# ================================================================
#   CODVEDA PYTHON INTERNSHIP - LEVEL 3, TASK 3
#   N-Queens Problem
#   Algorithm: Backtracking
#
#   HOW TO RUN:
#       python task3_nqueens.py
#   (No external libraries needed!)
# ================================================================


# ================================================================
#   STEP 1 — SAFETY CHECK
#   Check if placing a queen at (row, col) is safe.
#   We only check rows ABOVE current row (queens placed top→bottom)
# ================================================================

def is_safe(board, row, col, n):

    # ── Check same COLUMN (all rows above) ──────────────────────
    for i in range(row):
        if board[i][col] == 1:
            return False

    # ── Check upper-LEFT diagonal ───────────────────────────────
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

    # ── Check upper-RIGHT diagonal ──────────────────────────────
    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if board[i][j] == 1:
            return False
        i -= 1
        j += 1

    return True   # ✅ Safe to place a queen here


# ================================================================
#   STEP 2 — BACKTRACKING SOLVER
#   Tries to place a queen in every column of the current row.
#   → If safe: place queen, recurse to next row
#   → If stuck: remove queen (backtrack), try next column
#   → If all N rows filled: save solution
# ================================================================

def solve(board, row, n, all_solutions):

    # ── Base case: all N queens placed successfully ──────────────
    if row == n:
        all_solutions.append([r[:] for r in board])  # save deep copy
        return

    # ── Try every column in current row ─────────────────────────
    for col in range(n):
        if is_safe(board, row, col, n):

            board[row][col] = 1                       # Place queen ♛
            solve(board, row + 1, n, all_solutions)   # Recurse next row
            board[row][col] = 0                       # Backtrack ✗


# ================================================================
#   STEP 3 — ENTRY POINT
# ================================================================

def solve_nqueens(n):
    board         = [[0] * n for _ in range(n)]      # N×N board of 0s
    all_solutions = []
    solve(board, 0, n, all_solutions)
    return all_solutions


# ================================================================
#   DISPLAY — Print a single chessboard solution
# ================================================================

def display_board(board, n, number):
    print(f"\n  ── Solution #{number} " + "─" * (30 - len(str(number))))
    print("  +" + "───+" * n)

    for row in range(n):
        row_str = "  |"
        for col in range(n):
            row_str += " Q |" if board[row][col] == 1 else " . |"
        print(row_str)
        print("  +" + "───+" * n)

    # Show queen positions
    positions = [
        f"Row{row+1}→Col{col+1}"
        for row in range(n)
        for col in range(n)
        if board[row][col] == 1
    ]
    print(f"  ♛  {' | '.join(positions)}")


# ================================================================
#   DISPLAY — Results summary
# ================================================================

KNOWN_SOLUTIONS = {
    1: 1,  2: 0,  3: 0,   4: 2,    5: 10,
    6: 4,  7: 40, 8: 92,  9: 352, 10: 724,
   11: 2680, 12: 14200
}

def display_summary(n, count, elapsed):
    print(f"\n  {'═'*50}")
    print(f"  {'N-QUEENS RESULT SUMMARY':^50}")
    print(f"  {'═'*50}")
    print(f"  Board Size        :  {n} × {n}")
    print(f"  Total Solutions   :  {count}")
    if n in KNOWN_SOLUTIONS:
        match = "✅ Correct" if count == KNOWN_SOLUTIONS[n] else "❌ Mismatch"
        print(f"  Expected          :  {KNOWN_SOLUTIONS[n]}  →  {match}")
    print(f"  Time Taken        :  {elapsed:.6f} seconds")
    print(f"  {'═'*50}")


# ================================================================
#   MAIN PROGRAM
# ================================================================

def main():
    import time

    print("\n" + "=" * 55)
    print("          N - Q U E E N S   P R O B L E M")
    print("          Codveda Python Internship · Level 3")
    print("          Algorithm: Backtracking")
    print("=" * 55)

    print("""
  OBJECTIVE:
  ──────────
  Place N queens on an N×N chessboard such that
  NO two queens can attack each other.

  CONSTRAINTS:
  ────────────
   ✔  No two queens in the same ROW
   ✔  No two queens in the same COLUMN
   ✔  No two queens on the same DIAGONAL
    """)

    # Reference table
    print("  ┌────────────────────────────────────────┐")
    print("  │    N  │  Total Solutions               │")
    print("  ├────────────────────────────────────────┤")
    highlights = {4: " ← easy", 8: " ← classic", 12: " ← hard"}
    for k, v in KNOWN_SOLUTIONS.items():
        note = highlights.get(k, "")
        print(f"  │    {k:<3} │  {v:<6}{note:<28}│")
    print("  └────────────────────────────────────────┘")

    while True:
        print("\n  " + "─" * 45)

        # ── Get N from user ────────────────────────────────────
        try:
            n = int(input("  Enter N (1–12 recommended): ").strip())
        except ValueError:
            print("  ❌  Invalid input. Please enter a number.")
            continue

        if n < 1:
            print("  ❌  N must be at least 1.")
            continue

        if n > 12:
            print(f"  ⚠️   N={n} may take a long time to compute.")
            confirm = input("  Continue? (yes/no): ").strip().lower()
            if confirm != "yes":
                continue

        # ── Solve ──────────────────────────────────────────────
        print(f"\n  ⏳  Solving {n}-Queens using backtracking ...")
        start     = time.time()
        solutions = solve_nqueens(n)
        elapsed   = time.time() - start

        # ── Show summary ───────────────────────────────────────
        display_summary(n, len(solutions), elapsed)

        if not solutions:
            print(f"\n  ℹ️   No solution exists for N = {n}.")
            if n in (2, 3):
                print("  (Mathematically proven: N=2 and N=3 have zero solutions)")

        else:
            # ── Ask how many boards to print ───────────────────
            try:
                raw = input(f"\n  Display how many solutions? (1–{len(solutions)} or 'all'): ").strip().lower()
                show = len(solutions) if raw == "all" else max(1, min(int(raw), len(solutions)))
            except ValueError:
                show = 1

            for idx, sol in enumerate(solutions[:show], 1):
                display_board(sol, n, idx)

            remaining = len(solutions) - show
            if remaining > 0:
                print(f"\n  ... {remaining} more solution(s) exist but were not displayed.")

        # ── Again? ─────────────────────────────────────────────
        again = input("\n  Solve for a different N? (yes / no): ").strip().lower()
        if again != "yes":
            print("\n  👋  Goodbye!\n")
            break


if __name__ == "__main__":
    main()
