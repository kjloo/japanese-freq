import React, { FunctionComponent } from "react";
import styles from "./FuriganaMessage.module.css";

interface FuriganaMessageProps {
  text: string;
}

// Matches Kanji/text attached to bracketed furigana: 習慣[しゅうかん] or 及ぼす[およぼす]
const BRACKETED_FURIGANA_REGEX = /([^\s[\]]+)\[([^\]]+)\]/g;

const FuriganaMessage: FunctionComponent<FuriganaMessageProps> = ({ text }) => {
  // Split input string by spaces to parse word tokens
  const words = text.split(" ");

  const renderWord = (word: string): React.ReactNode[] => {
    const nodes: React.ReactNode[] = [];
    let lastIndex = 0;
    let match: RegExpExecArray | null;

    // Reset regex index state
    BRACKETED_FURIGANA_REGEX.lastIndex = 0;

    while ((match = BRACKETED_FURIGANA_REGEX.exec(word)) !== null) {
      const matchStart = match.index;
      const baseText = match[1];
      const reading = match[2];

      // Add plain text preceding this match (if any)
      if (matchStart > lastIndex) {
        nodes.push(
          <span key={`text-${lastIndex}`}>
            {word.slice(lastIndex, matchStart)}
          </span>,
        );
      }

      // Add correctly nested <ruby> element
      nodes.push(
        <ruby key={`ruby-${matchStart}`} className={styles.rubyContainer}>
          {baseText}
          <rt className={styles.furiganaText}>{reading}</rt>
        </ruby>,
      );

      lastIndex = BRACKETED_FURIGANA_REGEX.lastIndex;
    }

    // Add trailing text after the last match (if any)
    if (lastIndex < word.length) {
      nodes.push(
        <span key={`text-${lastIndex}`}>{word.slice(lastIndex)}</span>,
      );
    }

    return nodes;
  };

  return (
    <span className={styles.messageContainer}>
      {words.map((word, wordIndex) => (
        <React.Fragment key={wordIndex}>{renderWord(word)}</React.Fragment>
      ))}
    </span>
  );
};

export default FuriganaMessage;
