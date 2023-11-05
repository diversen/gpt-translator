import sqlite3
import os

class DB:

    def __init__(self, working_dir):
        # create database if it doesn't exist
        self.db = sqlite3.connect(os.path.join(working_dir, "translation.db"))

        """
        create paragraphs table if it doesn't exist
        With idx (the primary key) so that we can keep track of which paragraphs have been translated
        paragraph: the original paragraph
        translated: the translated paragraph
        """

        self.db.execute(
            """
            CREATE TABLE IF NOT EXISTS paragraphs (
                idx INTEGER PRIMARY KEY,
                paragraph TEXT NOT NULL,
                translated TEXT
            )
            """
        )

    def idx_is_translated(self, idx):
        cursor = self.db.execute(
            """
            SELECT COUNT(*) FROM paragraphs WHERE idx = ? AND translated IS NOT NULL
            """,
            (idx,),
        )
        total = cursor.fetchone()[0]
        return total > 0
    
    def get_paragraph(self, idx):
        cursor = self.db.execute(
            """
            SELECT paragraph FROM paragraphs WHERE idx = ?
            """,
            (idx,),
        )
        return cursor.fetchone()[0]

    def idx_exists(self, idx):
        cursor = self.db.execute(
            """
            SELECT COUNT(*) FROM paragraphs WHERE idx = ?
            """,
            (idx,),
        )
        total = cursor.fetchone()[0]
        return total > 0

    def insert_paragraph(self, idx, paragraph):

        # check it row already exists
        if self.idx_exists(idx):
            return

        self.db.execute(
            """
            INSERT INTO paragraphs (idx, paragraph)
            VALUES (?, ?)
            """,
            (idx, paragraph),
        )
        self.db.commit()

    def update_paragraph_translation(self, idx, translated):
        self.db.execute(
            """
            UPDATE paragraphs
            SET translated = ?
            WHERE idx = ?
            """,
            (translated, idx),
        )
        self.db.commit()
        
    def get_count_paragraphs(self):
        """
        Get total count of paragraphs
        """
        cursor = self.db.execute(
            """
            SELECT COUNT(*) FROM paragraphs
            """
        )
        total = cursor.fetchone()[0]
        return total
    
    def all_translated(self):
        """
        Check if all paragraphs have been translated
        """
        cursor = self.db.execute(
            """
            SELECT COUNT(*) FROM paragraphs WHERE translated IS NOT NULL
            """
        )
        total = cursor.fetchone()[0]
        return total == self.get_count_paragraphs()
    
    def get_idxs(self):
        """
        Get all indexes
        """
        cursor = self.db.execute(
            """
            SELECT idx FROM paragraphs
            """
        )
        return [idx[0] for idx in cursor.fetchall()]
    
    def get_all_rows(self):

        # set connection to associate rows with columns
        self.db.row_factory = sqlite3.Row
        """
        Get all rows
        """
        cursor = self.db.execute(
            """
            SELECT * FROM paragraphs
            """
        )
        
        return cursor.fetchall()
        