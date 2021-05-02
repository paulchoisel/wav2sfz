import os
import pygubu
import tkinter as tk

from importlib import resources
from tkinter import filedialog, ttk

from .wav2sfz import convertWav2sfz


class wav2sfzApp(pygubu.TkApplication):

    def __init__(self, root):
        super(wav2sfzApp, self).__init__(root)

        # Create the UI
        self.builder = pygubu.Builder()
        self.builder.add_from_file(os.path.join(resources.files('wav2sfz'), 'UI/ui.ui'))

        # Apply the style (https://github.com/TkinterEP/ttkthemes/tree/master/ttkthemes/themes)
        root.tk.call('source', os.path.join(resources.files('wav2sfz'), 'UI/yaru/yaru.tcl'))
        guiStyle = ttk.Style()
        guiStyle.theme_use('yaru')

        # Set the window title
        self.set_title("Wav2sfz")

        # Store a reference to the root frame
        self.mainWindow = self.builder.get_object('mainFrame')

        # Input fields
        self.waveFileEntry = self.builder.get_object('waveFileEntry')
        self.tempoEntry = self.builder.get_object('tempoSpinbox')
        self.soundfontFolderEntry = self.builder.get_object('soundfontFolderEntry')
        self.musicXMLPathEntry = self.builder.get_object('musicXMLPathEntry')

        self.builder.connect_callbacks(self)

    @staticmethod
    def setEntryText(entry, text):
        entry.delete(0, tk.END)
        entry.insert(0, text)

    def convertWavFile(self):
        convertWav2sfz(
            self.waveFileEntry.get(),
            int(self.tempoEntry.get()),
            4,
            self.soundfontFolderEntry.get(),
            self.musicXMLPathEntry.get()
        )

    def browseWaveFile(self):
        self.setEntryText(self.waveFileEntry, filedialog.askopenfilename(
            filetypes=[('Wave file', '*.wav')]))

    def browseSoundfontFolder(self):
        self.setEntryText(self.soundfontFolderEntry, filedialog.askdirectory())

    def browseMusicXMLFile(self):
        self.setEntryText(self.musicXMLPathEntry, filedialog.asksaveasfilename(
            initialfile="result.musicxml"))

    def run(self):
        self.mainWindow.mainloop()


def main():
    root = tk.Tk()
    app = wav2sfzApp(root)
    app.run()


if __name__ == '__main__':
    main()
