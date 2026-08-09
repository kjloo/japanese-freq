import { render } from "@testing-library/react";
import { describe, it, expect } from "vitest"; // or 'jest' depending on your test runner
import FuriganaMessage from "../FuriganaMessage";

describe("FuriganaMessage", () => {
  it("renders a single bracketed furigana pair correctly", () => {
    const { container } = render(<FuriganaMessage text="今後[こんご]も" />);

    const rubyEl = container.querySelector("ruby");
    expect(rubyEl).not.toBeNull();
    expect(rubyEl).toHaveTextContent("今後こんご");

    const rtEl = container.querySelector("rt");
    expect(rtEl).not.toBeNull();
    expect(rtEl).toHaveTextContent("こんご");
  });

  it("handles complex sentences with space delimiters and multiple furigana tokens", () => {
    const text =
      "ところが、この 習慣[しゅうかん]が 健康[けんこう]に 大[おお]きな 影響[えいきょう]を 及ぼす[およぼす]ことが 分[わ]かってきました。";
    const { container } = render(<FuriganaMessage text={text} />);

    const rubyElements = container.querySelectorAll("ruby");
    expect(rubyElements).toHaveLength(5);

    const expectedPairs = [
      { base: "習慣", reading: "しゅうかん" },
      { base: "健康", reading: "けんこう" },
      { base: "大", reading: "おお" },
      { base: "影響", reading: "えいきょう" },
      { base: "及ぼす", reading: "およぼす" },
    ];

    rubyElements.forEach((ruby, index) => {
      const rt = ruby.querySelector("rt");
      expect(rt).not.toBeNull();
      expect(rt).toHaveTextContent(expectedPairs[index].reading);
      expect(ruby.textContent).toContain(expectedPairs[index].base);
    });
  });

  it("joins space-delimited words into a continuous string without extra spaces", () => {
    const { container } = render(
      <FuriganaMessage text="漢字[かんじ] を 勉強[べんきょう] する" />,
    );
    // Verify that space delimiters between words are stripped from the visible output
    expect(container.textContent).toBe("漢字かんじを勉強べんきょうする");
  });

  it("renders plain Japanese text without any bracketed furigana", () => {
    const { container } = render(
      <FuriganaMessage text="これは普通のエラーなしのテキストです。" />,
    );

    expect(container.querySelectorAll("ruby")).toHaveLength(0);
    expect(container.textContent).toBe(
      "これは普通のエラーなしのテキストです。",
    );
  });

  it("handles multiple bracketed furigana within a single word (no spaces between tokens)", () => {
    const { container } = render(
      <FuriganaMessage text="日本語[にほんご]学習[がくしゅう]" />,
    );

    const rubyElements = container.querySelectorAll("ruby");
    expect(rubyElements).toHaveLength(2);

    expect(rubyElements[0].querySelector("rt")).toHaveTextContent("にほんご");
    expect(rubyElements[1].querySelector("rt")).toHaveTextContent("がくしゅう");
  });

  it("renders bracketed terms without preceding base text as plain text", () => {
    const { container } = render(<FuriganaMessage text="[ごはん]は" />);

    expect(container.querySelectorAll("ruby")).toHaveLength(0);
    expect(container.textContent).toBe("[ごはん]は");
  });

  it("handles leading and trailing plain text around ruby elements", () => {
    const { container } = render(<FuriganaMessage text="前 赤[あか] 後" />);

    const ruby = container.querySelector("ruby");
    expect(ruby).not.toBeNull();
    expect(ruby?.querySelector("rt")).toHaveTextContent("あか");

    // Check full output text ordering
    expect(container.textContent).toBe("前赤あか後");
  });

  it("handles empty strings and strings containing only whitespace gracefully", () => {
    const { container: emptyContainer } = render(<FuriganaMessage text="" />);
    expect(emptyContainer.textContent).toBe("");

    const { container: spaceContainer } = render(
      <FuriganaMessage text="   " />,
    );
    expect(spaceContainer.textContent).toBe("");
  });

  it("renders non-Japanese text, numbers, and punctuation correctly alongside furigana", () => {
    const { container } = render(
      <FuriganaMessage text="第1[だいいち]章: Python3.13[ぱいそん]！" />,
    );

    const rubyElements = container.querySelectorAll("ruby");
    expect(rubyElements).toHaveLength(2);

    expect(rubyElements[0].textContent).toContain("第1だいいち");
    expect(rubyElements[1].textContent).toContain("Python3.13ぱいそん");
    expect(container.textContent).toBe("第1だいいち章: Python3.13ぱいそん！");
  });
});
