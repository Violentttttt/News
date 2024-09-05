def get_rate(title, available_ratings):
    ratings = ', '.join(map(str, available_ratings))

    prompt = (f"Given the news title '{title}', please rate the importance of the news on a scale from 1 to 10, "
              f"where 10 means extremely important news (like 'Pasha Durov has been imprisoned'). "
              f"Do not use any rating that has already been assigned. Available ratings are: {ratings} , 10. "
              f"Return only the rating as a number without additional text.")

    return prompt


def add_comment(post):
    prompt = (
        "USE SPACES BETWEEN TITLE , SUMMARY AND AI COMMENT"
        f"Study the news article at this link: {post.url}. "
        f"Write a detailed news summary and provide an engaging comment about the news in around 100"
        f"Include emojis if relevant and make sure the comment reflects your genuine reaction. "
        f"Use the following model to structure your response: "
        f"{post.title} "
        f" [Detailed summary of the news] "
        f"AI Comment: [Your engaging comment about the news] "
        f"Example: "
        f"Polygon to Start Much-Awaited Swap of POL Token for Longstanding MATIC "
        "free space"
        f"Summary: Polygon, a leading Ethereum scaling platform, is set to begin the highly anticipated swap of its POL token for the longstanding Matic token. This move is expected to simplify the network's token economy and provide a more streamlined experience for users. "
        "free space"
        f"AI Comment: I'm thrilled to see Polygon taking this huge step forward! 🤩 The token swap is a game-changer for the network, and I'm excited to see how it will propel the ecosystem to new heights! 🚀'"
        "#violent #polygon"
        "reurn me ONLY response , whithout optional words . As in Example"
        f"Your comment should be around 30 words. Write it with emotions. For example on tiding , that Pasha Durov go in prizon - you can make comment:'this world become crazy...")

    return prompt


