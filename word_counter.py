# ============================================
# TASK 3: Word Counter
# Codveda Python Internship - Level 1
# ============================================

def count_words(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()

            if not content.strip():
                print("The file is empty! No words to count.")
                return

            # Split into words and count
            words = content.split()
            word_count = len(words)

            # Extra useful stats
            lines = content.splitlines()
            line_count = len(lines)
            char_count = len(content)
            char_no_spaces = len(content.replace(" ", "").replace("\n", ""))

            print("=" * 40)
            print("         WORD COUNTER RESULTS")
            print("=" * 40)
            print(f"File Name       : {filename}")
            print(f"Total Words     : {word_count}")
            print(f"Total Lines     : {line_count}")
            print(f"Total Characters: {char_count}")
            print(f"Chars (no space): {char_no_spaces}")
            print("=" * 40)

            # Show top 5 most common words (bonus feature)
            word_frequency = {}
            for word in words:
                clean_word = word.lower().strip('.,!?";:()[]')
                word_frequency[clean_word] = word_frequency.get(clean_word, 0) + 1

            sorted_words = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)

            print("\nTop 5 Most Common Words:")
            for i, (word, count) in enumerate(sorted_words[:5], 1):
                print(f"  {i}. '{word}' - {count} time(s)")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        print("Please check the filename and try again.")
    except PermissionError:
        print(f"Error: You don't have permission to read '{filename}'.")
    except Exception as e:
        print(f"Unexpected error: {e}")


def word_counter_app():
    print("=" * 40)
    print("          WORD COUNTER APP")
    print("=" * 40)

    filename = input("Enter the filename (e.g., sample.txt): ").strip()
    count_words(filename)

    # Ask if user wants to count another file
    again = input("\nCount words in another file? (yes/no): ").lower()
    if again == 'yes':
        word_counter_app()
    else:
        print("\nGoodbye!")


# ---- Create a sample text file for testing ----
def create_sample_file():
    sample_text = """Python is a great programming language.
It is easy to learn and very powerful.
Python is used in web development, data science, and AI.
Many developers love Python because it is simple and clean.
Learning Python opens many opportunities in the tech industry."""

    with open("sample.txt", "w") as f:
        f.write(sample_text)
    print("[OK] sample.txt created for testing!\n")


# Create sample file then run app
create_sample_file()
word_counter_app()
