from jtech.gui.dialogs.dlg_dependencies import DependencySelectionDialog


class DependencyActionEvent:

    def selected_dependencies(self, parent_frame):
        dialog = DependencySelectionDialog(parent_frame)
        dialog.exec_()
        return dialog.get_selected_dependencies()
