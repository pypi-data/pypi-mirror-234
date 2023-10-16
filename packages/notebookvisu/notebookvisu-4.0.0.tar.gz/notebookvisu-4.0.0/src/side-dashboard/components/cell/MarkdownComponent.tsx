import React, { useState, useEffect } from 'react';
import { IMarkdownTranslator } from '../../../plugins/sideDashboard';

const MarkdownComponent = (props: {
  markdownContent: string;
  markdownTranslator: IMarkdownTranslator;
}) => {
  const [sanitizedContent, setSanitizedContent] = useState<string | null>(null);

  useEffect(() => {
    const parseContent = async () => {
      const parsedResult = await props.markdownTranslator.markdownParser.render(
        props.markdownContent
      );
      setSanitizedContent(
        props.markdownTranslator.sanitizer.sanitize(parsedResult)
      );
    };
    parseContent();
  }, [props.markdownContent]);

  return (
    <div className="cell-content-container">
      {sanitizedContent && (
        <div
          className="jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput"
          dangerouslySetInnerHTML={{ __html: sanitizedContent }}
        />
      )}
    </div>
  );
};

export default MarkdownComponent;
