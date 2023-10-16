import os
import sqlite3
from typing import Protocol

from ..schema import (ChatCompletionUsage, CompletionUsage, EmbeddingUssage,
                      Message)


class MemoryProtocol(Protocol):
    namespace: str

    async def query(self, text: str, top_k: int) -> list[str]:
        ...

    async def upsert(self, messages:list[Message]) -> None:
        ...

    async def fetch(self) -> list[Message]:
        ...


class SqliteMemory(MemoryProtocol):
    def __init__(self, namespace: str):
        if not os.path.exists(".cache"):
            os.mkdir(".cache")
        self.namespace = namespace
        self.connection = sqlite3.connect(f".cache/{namespace}.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            """
			CREATE TABLE IF NOT EXISTS memory (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				role TEXT NOT NULL,
                text TEXT NOT NULL
			);
			"""
        )
        self.cursor.execute(
            """
			CREATE TABLE IF NOT EXISTS chat_completion_usage (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				prompt_tokens INTEGER NOT NULL,
				completion_tokens INTEGER NOT NULL,
				total_tokens INTEGER NOT NULL
			);
			"""
        )
        self.cursor.execute(
            """
			CREATE TABLE IF NOT EXISTS completion_usage (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				prompt_tokens INTEGER NOT NULL,
				completion_tokens INTEGER NOT NULL,
				total_tokens INTEGER NOT NULL
			);
			"""
        )
        self.cursor.execute(
            """
			CREATE TABLE IF NOT EXISTS image (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				text TEXT NOT NULL,
				url TEXT NOT NULL
			);
			"""
        )
        self.cursor.execute(
            """
			CREATE TABLE IF NOT EXISTS audio (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				duration INTEGER NOT NULL,
				text TEXT NOT NULL
			);
			"""
        )
        self.cursor.execute(
            """
			CREATE TABLE IF NOT EXISTS embeddings_usage (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				prompt_tokens INTEGER NOT NULL,
				completion_tokens INTEGER NOT NULL,
				total_tokens INTEGER NOT NULL
			);
			"""
        )
        self.connection.commit()

    async def query(self, text: str, top_k: int) -> list[str]:
        self.cursor.execute(
            """
			SELECT text FROM memory
            WHERE text LIKE ?
            ORDER BY RANDOM()
            LIMIT ?;
			""",
            (f"%{text}%", top_k),
        )
        return [i[0] for i in self.cursor.fetchall()]

    async def upsert(self, messages: list[Message]) -> None:
        self.cursor.executemany(
            """
            INSERT INTO memory (text, role)
            VALUES (?, ?);
            """,
            [(message.content, message.role) for message in messages],
        )
        self.connection.commit()
        

    async def save_chat_completion_usage(self, usage: ChatCompletionUsage) -> None:
        self.cursor.execute(
            """
			INSERT INTO chat_completion_usage (prompt_tokens, completion_tokens, total_tokens)
			VALUES (?, ?, ?);
			""",
            (usage.prompt_tokens, usage.completion_tokens, usage.total_tokens),
        )
        self.connection.commit()

    async def save_completion_usage(self, usage: CompletionUsage) -> None:
        self.cursor.execute(
            """
			INSERT INTO completion_usage (prompt_tokens, completion_tokens, total_tokens)
			VALUES (?, ?, ?);
			""",
            (usage.prompt_tokens, usage.completion_tokens, usage.total_tokens),
        )
        self.connection.commit()

    async def save_embeddings_usage(self, usage: EmbeddingUssage) -> None:
        self.cursor.execute(
            """
			INSERT INTO embeddings_usage (prompt_tokens, completion_tokens, total_tokens)
			VALUES (?, ?, ?);
			""",
            (usage.prompt_tokens, usage.completion_tokens, usage.total_tokens),
        )
        self.connection.commit()

    async def save_image(self, text: str, url: str) -> None:
        self.cursor.execute(
            """
			INSERT INTO image (text, url)
			VALUES (?, ?);
			""",
            (text, url),
        )
        self.connection.commit()

    async def save_audio(self, duration: int, text: str) -> None:
        self.cursor.execute(
            """
			INSERT INTO audio (duration, text)
			VALUES (?, ?);
			""",
            (duration, text),
        )
        self.connection.commit()

    async def fetch(self) -> list[Message]:
        self.cursor.execute(
            """
			SELECT * FROM memory;
		
			"""
        )
        return [Message(role=i[1], content=i[2]) for i in self.cursor.fetchall()]

    async def fetch_chat_completion_usage(self) -> list[ChatCompletionUsage]:
        self.cursor.execute(
            """
			SELECT * FROM chat_completion_usage;
			"""
        )
        return [
            ChatCompletionUsage(
                prompt_tokens=i[1], completion_tokens=i[2], total_tokens=i[3]
            )
            for i in self.cursor.fetchall()
        ]

    async def fetch_completion_usage(self) -> list[CompletionUsage]:
        self.cursor.execute(
            """
			SELECT * FROM completion_usage;
			"""
        )
        return [
            CompletionUsage(
                prompt_tokens=i[1], completion_tokens=i[2], total_tokens=i[3]
            )
            for i in self.cursor.fetchall()
        ]

    async def fetch_embeddings_usage(self) -> list[EmbeddingUssage]:
        self.cursor.execute(
            """
			SELECT * FROM embeddings_usage;
			"""
        )
        return [
            EmbeddingUssage(
                prompt_tokens=i[1], completion_tokens=i[2], total_tokens=i[3]
            )
            for i in self.cursor.fetchall()
        ]

    async def fetch_image(self) -> list[tuple[str, str]]:
        self.cursor.execute(
            """
			SELECT * FROM image;
			"""
        )
        return [(i[1], i[2]) for i in self.cursor.fetchall()]

    async def fetch_audio(self) -> list[tuple[int, str]]:
        self.cursor.execute(
            """
			SELECT * FROM audio;
			"""
        )
        return [(i[1], i[2]) for i in self.cursor.fetchall()]
