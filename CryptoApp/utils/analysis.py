from collections import Counter
import pandas as pd


def analyze_text(content, treeview):
    """Analyze the text and display character frequency."""
    if not content:
        return

    content = ''.join(c.lower() for c in content if c.isalpha())
    char_counts = Counter(content)
    total_chars = sum(char_counts.values())

    frequency_data = pd.DataFrame(
        [(char, count, count / total_chars) for char, count in char_counts.items()],
        columns=["Character", "Count", "Frequency"]
    )

    frequency_data.sort_values(by="Frequency", ascending=False, inplace=True)

    treeview.delete(*treeview.get_children())

    for index, row in frequency_data.iterrows():
        tag = "evenrow" if index % 2 == 0 else "oddrow"
        treeview.insert("", "end", values=(row["Character"], row["Count"], f"{row['Frequency'] * 100:.2f}%"),
                        tags=(tag,))