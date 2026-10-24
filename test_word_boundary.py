import asyncio
import edge_tts

async def main():
    comm = edge_tts.Communicate("Why your CCTV night vision turns white when someone walks past.", "en-GB-RyanNeural")
    words = []
    async for chunk in comm.stream():
        if chunk["type"] == "WordBoundary":
            words.append((chunk["offset"] / 10_000_000, chunk["duration"] / 10_000_000, chunk["text"]))
    print(f"Captured {len(words)} words:")
    for w in words[:6]:
        print(f"  {w[0]:.2f}s - {w[0]+w[1]:.2f}s: {w[2]}")

if __name__ == "__main__":
    asyncio.run(main())
