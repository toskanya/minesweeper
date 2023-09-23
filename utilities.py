import settings

def height_prct(percentage):
    return (settings.HEIGHT / 100) * percentage

def width_prct(percentage):
    return (settings.WIDTH / 100) * percentage

def get_widget_size(widget):
    return widget.winfo_width(), widget.winfo_height()

is_on = False
def toggle(minesweeperAI):
    global is_on
    is_on = not is_on
    if is_on:
        minesweeperAI.start()
    else:
        minesweeperAI.stop()