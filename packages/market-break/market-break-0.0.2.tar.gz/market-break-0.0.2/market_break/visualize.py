# visualize.py

import tkinter as tk
import sys
from PIL import Image, ImageTk
import os
import warnings
from typing import (
    Iterable, Dict, Optional, Union, Callable, Any
)

import pandas as pd
import matplotlib.pyplot as plt

from market_break.process import up_movement, down_movement
from market_break.evaluation import results_report, EvaluationResults
from market_break.utils.base import assets

__all__ = [
    "EvaluationResultsWindow",
    "report_repr",
    "visualize_evaluation_results_plot",
    "visualize_evaluation_results_window"
]

if 'win' in sys.platform:
    from ctypes import windll

    app_id_stamp = (
        'ArbitrageScreener.application.Desktop-Application.1.0'
    )

    windll.user32.ShowWindow(
        windll.kernel32.GetConsoleWindow(), False
    )
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        app_id_stamp
    )
# end if

plt.style.core.update_nested_dict(
    plt.style.library,
    plt.style.core.read_style_directory(
        f"{assets()}\\themes\\"
    )
)

def report_repr(
        data: Dict[str, Union[str, float]], title: Optional[str] = None
) -> str:
    """
    Returns a string representation of the results.

    :param data: The data to convert into a string.
    :param title: The title of the window.

    :return: The string representation of the data.
    """

    index = [0]

    for i, value in enumerate(data.values(), start=1):
        if value != "":
            index.append(index[-1] + 1)

        else:
            index.append(index[-1])
        # end if
    # end for

    return (
        "\n" + title + "\n\n" if isinstance(title, str) else ""
    ) + "\n".join(
        [
            (
                f"[{i}]{' ': <{3 - len(str(i))}}"
                f"{message: <35}" if value != '' else f'\n{message}'
            ) +
            f"{str(value if isinstance(value, str) else round(value, 3))}"
            for i, (message, value) in zip(index[1:], data.items())
        ]
    ) + "\n"
# end report_repr

class EvaluationResultsWindow(tk.Toplevel):
    """
    A class to represent a results window.

    The object to create and display a window to show the results
    of the simulation process.

    - results:
        The results object to display its data.

    - title:
        The title of the window to display.

    - theme:
        The theme of the window to display.

    - symbols:
        The symbols of the assets.

    - icon:
        The icon for the window.

    >>> from market_break.visualize import EvaluationResultsWindow
    >>>
    >>> EvaluationResultsWindow(...).mainloop()
    """

    parent = None

    def __init__(
            self,
            results: Optional[EvaluationResults] = None,
            title: Optional[str] = None,
            theme: Optional[str] = None,
            icon: Optional[str] = None,
            image: Optional[str] = None
    ) -> None:
        """
        Defines the class attributes.

        :param results: The results object.
        :param title: The title of the window.
        :param theme: The theme of the window.
        :param icon: The icon for the window.
        :param image: The path to the image file.
        """

        if EvaluationResultsWindow.parent is None:
            EvaluationResultsWindow.parent = tk.Tk()

            EvaluationResultsWindow.parent.withdraw()
        # end if

        super().__init__(EvaluationResultsWindow.parent)

        self.title_text: Optional[str] = title
        self.theme: Optional[str] = theme
        self.icon: Optional[str] = icon or f"{assets()}/icon/icon.ico"
        self.image: Optional[str] = image

        self.results: Optional[EvaluationResults] = results

        self.data: Dict[str, float] = {}

        self.build(
            results=results, title=title,
            theme=theme, icon=icon, image=image
        )
    # end __init__

    def __str__(self) -> str:
        """
        Returns a string representation of the object.

        :return: The string with the results.
        """

        return report_repr(
            data=self.data, title=self.title_text
        )
    # end __str__

    def build(
        self,
        results: EvaluationResults,
        title: Optional[str] = None,
        theme: Optional[str] = None,
        icon: Optional[str] = None,
        image: Optional[str] = None
    ) -> None:
        """
        Defines the class attributes.

        :param results: The results object.
        :param title: The title of the window.
        :param theme: The theme of the window.
        :param icon: The icon for the window.
        :param image: The path to the image file.
        """

        try:
            previous = self.winfo_children()

            if title:
                self.title_text = title
            # end if

            if theme:
                self.theme = theme
            # end if

            if icon:
                self.icon = icon
            # end if

            if image:
                self.image = image
            # end if

            title = title or self.title_text or f"Arbitrage Results"
            theme = theme or self.theme or "light"
            image = image or self.image

            self.title(title)
            self.iconbitmap(
                (
                    icon if (icon is not None and os.path.exists(icon)) else None
                ) or self.icon or f"{assets()}/icon/icon.ico"
            )

            self.results = results or self.results or EvaluationResults()

            if theme == "dark":
                bg = "#151515"
                fg = "#FFFFFF"

                self.config(bg=bg)

            elif theme == "light":
                fg = "#151515"
                bg = "#FFFFFF"

                self.config(bg=bg)

            else:
                bg = None
                fg = None
            # end if

            self.data = results_report(results=self.results)

            root = self

            frames = []

            for i, (message, value) in enumerate(self.data.items()):
                i: int

                if value == "":
                    root = tk.Frame(self, bg=bg)

                    root.grid_columnconfigure(0, weight=1)
                    root.grid_columnconfigure(1, weight=1)

                    frames.append(root)

                    tk.Label(
                        root, bg=bg, fg=fg, text=str(message),
                        font=("Ariel", 15, "bold")
                    ).grid(
                        row=i, column=0, sticky="nsw", padx=20, columnspan=2,
                        pady=(10 if i != 0 else (20, 10))
                    )

                else:
                    tk.Label(
                        root, bg=bg, fg=fg, text=str(message), font=("Ariel", 13)
                    ).grid(
                        row=i, column=0, sticky="nsw", padx=(20, 10),
                        pady=(5 if i != 0 else (10, 5))
                    )
                    tk.Label(
                        root, bg=bg, fg="#00b5fa", font=("Ariel", 13),
                        text=str(value if isinstance(value, (str, int)) else f"{value:.3f}")
                    ).grid(
                        row=i, column=1, sticky="nse", padx=(10, 20),
                        pady=(5 if i != len(self.data) - 1 else (5, 10))
                    )
                # end if
            # end for

            left_frames = frames[:len(frames) // 2 + 1 - len(frames) % 2]
            right_frames = frames[len(frames) // 2:]

            if len(left_frames) == 1:
                right_frames = left_frames + right_frames
                left_frames = []
            # end if

            if left_frames:
                self.grid_columnconfigure(0, weight=1)
            # end if

            if right_frames:
                self.grid_columnconfigure(1, weight=1)
            # end if

            for i, frame in enumerate(left_frames):
                frame.grid(
                    row=i, column=0, sticky="nsew",
                    padx=(15, 0), pady=(
                        (0, 15) if (i == len(left_frames) - 1) else 0
                    )
                )
            # end for

            for i in range(max(len(right_frames), len(left_frames))):
                self.grid_rowconfigure(i, weight=1)
            # end for

            for i, frame in enumerate(right_frames):
                frame.grid(
                    row=i, column=1, sticky="nsew",
                    padx=(15, 0), pady=(
                        (0, 15) if (i == len(right_frames) - 1) else 0
                    )
                )
            # end for

            if image and os.path.exists(image):
                position = 1

                if left_frames:
                    position += 1
                # end if

                if right_frames:
                    position += 1
                # end if

                image_object = ImageTk.PhotoImage(Image.open(image))

                image_label = tk.Label(self, image=image_object)
                image_label.image = image_object

                image_label.grid(
                    row=0, column=position, sticky="nsew", padx=20, pady=20,
                    rowspan=max(len(left_frames), len(right_frames))
                )

                self.columnconfigure(position, weight=1)
            # end if

            for child in previous:
                child.destroy()
            # end for

        except tk.TclError:
            pass
        # end try
    # end build
# end SimulationResultsWindow

def visualize_evaluation_results_window(
        results: Optional[EvaluationResults] = None,
        title: Optional[str] = None,
        theme: Optional[str] = None,
        icon: Optional[str] = None
) -> EvaluationResultsWindow:
    """
    Defines the class attributes.

    :param results: The results object.
    :param title: The title of the window.
    :param theme: The theme of the window.
    :param icon: The icon for the window.
    """

    return EvaluationResultsWindow(
        results=results, title=title,
        theme=theme, icon=icon
    )
# end visualize_evaluation_results_window

def visualize_evaluation_results_plot(
        results: EvaluationResults,
        save: Optional[str] = None,
        additions: Optional[
            Union[
                Iterable[Callable[[], Any]],
                Dict[str, Iterable[float]],
                Iterable[Iterable[float]],
                bool
            ]
        ] = None,
        show: Optional[bool] = True,
        title: Optional[str] = None,
        trade_index: Optional[Iterable] = None,
        icon: Optional[str] = None,
        theme: Optional[str] = None,
) -> plt.Figure:
    """
    Visualizes the process results.

    :param results: The results object.
    :param save: The value to save the image.
    :param show: The value to show the image.
    :param theme: The theme of the window.
    :param additions: The additions to run to add to the plot.
    :param title: The title of the window.
    :param trade_index: The index for the plot.
    :param icon: The path to an icon.
    """

    icon = icon or f"{assets()}/icons/icon.ico"
    theme = theme or "light"

    additions = additions or {}
    commands = {}

    if theme:
        plt.style.use(theme)
    # end if

    warnings.resetwarnings()

    if isinstance(additions, dict):
        additions.update(commands)

    else:
        additions = [*additions, *commands.values()]
    # end if

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        plot = plt.figure(
            "Arbitrage Trading",
            figsize=(13 if additions else 10, 7.5 if additions else 6)
        )

    plt.subplots_adjust(
        top=0.938, bottom=0.067, right=0.974,
        left=0.06, hspace=0.283, wspace=0
    )

    labeled = False

    if additions:
        plt.subplot(2, 1, 1)
        plt.title(title or f"Arbitrage Trading Performance")

        for addition in additions:
            if (addition is not None) and callable(addition):
                addition()

            elif addition is not None:
                if isinstance(additions, dict):
                    if not callable(additions[addition]):
                        labeled = True

                        plt.plot(
                            (
                                list(range(len(additions[addition])))
                                if not isinstance(additions[addition], pd.Series)
                                else additions[addition].index
                            ),
                            additions[addition],
                            lw=1.25, label=addition
                        )

                    else:
                        additions[addition]()
                    # end if

                elif isinstance(addition, pd.Series):
                    labeled = True

                    plt.plot(
                        (
                            list(range(len(additions[addition])))
                            if not isinstance(addition, pd.Series)
                            else addition.index
                        ),
                        addition, lw=1.25, label=addition.name
                    )

                else:
                    plt.plot(list(range(len(addition))), addition, lw=1.25)
                # end if
            # end if
        # end for

        plt.xlabel("Time")
        plt.ylabel("Normalized Price Spread")

        if labeled:
            plt.legend()
        # end if
    # end if

    trade_index = trade_index or range(len(results.balances))

    plt.subplot(2 if additions else 1, 1, 2 if additions else 1)
    plt.title(
        title or (
            "Arbitrage Trading Results "
            f"({(results.balances[-1] / results.balances[0] - 1) * 100:.3f}%)"
        )
    )

    predictions = None

    if (results.predictions is not None) and (len(results.predictions) > 0):
        predictions = ((results.predictions / results.predictions[0]) - 1) * 100
    # end if

    balances = (results.balances / results.balances[0] - 1) * 100

    profits = up_movement(balances)
    losses = -down_movement(balances)

    if predictions is not None:
        plt.plot(trade_index, predictions, lw=1.25, label=f'Predicted Balance', color='blue')
        plt.fill_between(trade_index, predictions, balances, color="blue", alpha=0.1)
        plt.fill_between(trade_index, balances, predictions, color="blue", alpha=0.1)
    # end if

    plt.plot(trade_index, balances, lw=1.25, label=f'Balance', color='orange')
    plt.plot(trade_index, profits, lw=1.25, label=f'Profits', color='green')
    plt.plot(trade_index, losses, lw=1.25, label=f'Losses', color='red')

    plt.fill_between(trade_index, profits, balances, color="green", alpha=0.1)
    plt.fill_between(trade_index, balances, losses, color="yellow", alpha=0.1)
    plt.fill_between(trade_index, losses, color="red", alpha=0.1)
    plt.xlabel("Time")
    plt.ylabel("Produced Balance (%)")
    plt.legend()

    if save:
        if os.path.split(save)[0]:
            os.makedirs(os.path.split(save)[0], exist_ok=True)
        # end if

        plt.savefig(save)
    # end if

    if isinstance(icon, str) and os.path.exists(icon):
        manager = plt.get_current_fig_manager()

        # noinspection PyProtectedMember
        manager.window.tk.call('wm', 'iconbitmap', manager.window._w, icon)
    # end if

    warnings.resetwarnings()

    if show:
        plt.show()
    # end if

    return plot
# end visualize_evaluation_results_plot