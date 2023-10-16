import React, { useRef, useEffect } from 'react';
import { jupyterTheme, CodeMirrorEditor } from '@jupyterlab/codemirror';
import { CodeEditor } from '@jupyterlab/codeeditor';
import { EditorView } from '@codemirror/view';
import { editorDefaultLanguages } from '../../../utils/language';

interface ICellInputProps {
  cell_input: string;
  language_mimetype: string;
  className: string;
}

const CellInput = ({
  cell_input,
  language_mimetype,
  className
}: ICellInputProps): JSX.Element => {
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (container) {
      // clear the rendered HTML
      container.innerHTML = '';

      const model = new CodeEditor.Model();
      model.mimeType = language_mimetype;
      model.sharedModel.setSource(cell_input);
      // binds the editor to the host HTML element
      new CodeMirrorEditor({
        host: container,
        model: model,
        extensions: [
          jupyterTheme,
          EditorView.lineWrapping,
          EditorView.editable.of(false)
        ],
        languages: editorDefaultLanguages
      });
    }
  }, [cell_input, language_mimetype]);

  return <div ref={containerRef} className={className} />;
};

export default CellInput;
