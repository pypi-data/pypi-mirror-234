from enum import Enum
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import importlib.resources

LEGEND_SIZE = (1225, 3350)
V_PADDING = 40
H_PADDING = 60

SCALE_RATIO = 2

TITLE_FONT_SIZE = 75
ITEM_FONT_SIZE = 65

WHITE_TEXT_RGB = (221, 223, 232)
GRAY_TEXT_RGB = (39, 40, 43)

DETAIL_TEXT_RGB = (97, 100, 110)

SHAPE_RGB = (165, 169, 182)

H_OFFSET_ITEMS = 80

H_OFFSET_LEGEND_ITEMS = H_PADDING + H_OFFSET_ITEMS + 5

LEGEND_ITEM_CIRCLE_SIZE = 40
LEGEND_ITEM_INTRA_OFFSET = 20

RECTANGLE_TOTAL_WIDTH = LEGEND_SIZE[0] - H_PADDING * 2 - H_OFFSET_ITEMS * 2
RECTANGLE_TOTAL_HEIGHT = 80
DEFAULT_COLOR_GRADIENT_HEX = "045CF0FF, 47B0E7FF, 54DEA6FF, E6FE94FF, FBEA7DFF, FEA451FF, FE6C38FF, FF063AFF"

HEADER_FRAME_HEIGHT = 160


class GradientType(Enum):
    """
    Different types of gradient color legends
    """

    GRADIENT = "Gradient"
    POINT_DENSITY = "Point Density"
    HISTOGRAM = "Bin Size"  # [EXPD-2384]


def get_icon_name(shape):
    icon_name = shape["Shape Name"]

    point_shape_converter = {
        "Sphere": "Sphere",
        "Cube": "Cube",
        "Pyramid": "Crescent",
        "Cone": "Pyramid",
        "Wedge": "Plus",
        "Star": "Cross",
        "MissingValue": "MissingValue",
        "Count": "Count",
    }
    # Return an os relative path to the icon
    return f"Shape_{point_shape_converter[icon_name]}_512.png"


# All the different sizes are based on the figma design x10
class LegendBuilder:
    # Define the PIL image, PIL_legend_draw and fonts objects
    def __init__(self, legend_dict: dict, dark_theme: bool):
        # Define the theme
        self.dark_theme = dark_theme
        self.bg_color = self.get_legend_bg_color(self.dark_theme)

        # Define the PIL image, PIL_legend_draw and fonts objects
        self.PIL_legend_image = Image.new("RGB", LEGEND_SIZE, color=self.bg_color)
        self.PIL_legend_draw = ImageDraw.Draw(self.PIL_legend_image)

        # Import from virtualitics.assets the fonts
        with importlib.resources.path("virtualitics.assets", "Inter-Regular.ttf") as font_path:
            self.PIL_title_font = ImageFont.truetype(str(font_path), TITLE_FONT_SIZE)
            self.PIL_item_font = ImageFont.truetype(str(font_path), ITEM_FONT_SIZE)

        # Store the legend dict
        if "Color" not in legend_dict and "Shape" not in legend_dict:
            raise ValueError("Legend dict must contain at least one of Color or Shape")
        self.legend_dict = legend_dict

        # Incrementally draw the legend on the image object
        self.current_v_pointer = V_PADDING * 2
        if "Color" in self.legend_dict:
            self.draw_color_legend()

        if "Shape" in self.legend_dict:
            self.current_v_pointer += V_PADDING * 2
            self.draw_shape_legend()

    @staticmethod
    def get_legend_item_count(legend_item, numDenomIndex):
        # Fetching the color count: [0] stores the visible count, [1] stores the total count
        # Also, remove the comma from the total count for the int() conversion
        item_count = legend_item["Count"].split("/")[numDenomIndex].replace(",", "")
        return int(item_count)

    @staticmethod
    def sum_color_counts(color_legend, numDenomIndex):
        total = 0
        for color in color_legend:
            if "Color Hex" not in color or "Count" not in color:
                continue

            total += LegendBuilder.get_legend_item_count(color, numDenomIndex)
        return total

    @staticmethod
    def get_color_rgb_tuple(color_hex):
        return tuple(
            int(color_hex[color_drawing_counter : color_drawing_counter + 2], 16)
            for color_drawing_counter in (0, 2, 4, 6)
        )

    @staticmethod
    def get_legend_bg_color(dark_theme: bool):
        return (26, 26, 28) if dark_theme else (252, 252, 253)

    # Replace any occurrence of the old_color RGB tuple with the new_color
    @staticmethod
    def replace_color(image, old_color, new_color):
        image = image.convert("RGBA")
        data = image.getdata()
        new_data = []
        for item in data:
            if item[:3] == old_color:
                new_data.append(new_color + (255,))
            else:
                new_data.append(item)
        image.putdata(new_data)
        return image

    def get_legend_image(self):
        return self.PIL_legend_image

    def draw_color_legend(self):
        self.color_legend = self.legend_dict["Color"]
        gradient_type = None

        if "Point Density Original Min" in self.color_legend[0]:
            self.color_legend = self.color_legend[0]
            gradient_type = GradientType.POINT_DENSITY

            self.PIL_legend_draw.text(
                (H_PADDING + 25, self.current_v_pointer),
                gradient_type.value,
                fill=WHITE_TEXT_RGB if self.dark_theme else GRAY_TEXT_RGB,
                font=self.PIL_title_font,
            )
        elif "Bin Size Method" in self.color_legend[0]:  # [EXPD-2385]
            self.color_legend = self.color_legend[0]
            gradient_type = GradientType.HISTOGRAM

            self.PIL_legend_draw.text(
                (H_PADDING + 25, self.current_v_pointer),
                self.legend_dict["Color Column"] if "Color Column" in self.legend_dict else gradient_type.value,
                fill=WHITE_TEXT_RGB if self.dark_theme else GRAY_TEXT_RGB,
                font=self.PIL_title_font,
            )
        else:
            if "Gradient Original Min" in self.color_legend[0]:
                self.color_legend = self.color_legend[0]
                gradient_type = GradientType.GRADIENT

            # Load the Color Circle icon png and resize it
            with importlib.resources.path("virtualitics.assets", "ColorWheel_512.png") as circle_icon_path:
                color_circle_icon = Image.open(str(circle_icon_path)).resize((H_OFFSET_ITEMS, H_OFFSET_ITEMS))

                # Replace only black pixels with the rgb tuple of the bg color
                color_circle_icon = self.replace_color(color_circle_icon, (0, 0, 0), self.bg_color)

                self.PIL_legend_image.paste(color_circle_icon, (H_PADDING, self.current_v_pointer))
            self.PIL_legend_draw.text(
                (H_PADDING + H_OFFSET_ITEMS + 25, self.current_v_pointer),
                self.legend_dict["Color Column"],
                fill=WHITE_TEXT_RGB if self.dark_theme else GRAY_TEXT_RGB,
                font=self.PIL_title_font,
            )

        self.current_v_pointer += HEADER_FRAME_HEIGHT

        self.rectangle_current_h_offset = H_PADDING + H_OFFSET_ITEMS
        self.rectangle_current_v_offset = self.current_v_pointer

        self.current_v_pointer += RECTANGLE_TOTAL_HEIGHT + V_PADDING

        self.rectangle_portion_colored = 0

        if gradient_type is not None:
            self.draw_color_legend_gradient(gradient_type)
        else:
            self.draw_color_legend_items()

    def draw_color_legend_items(self):
        color_drawing_counter = 2
        numeratorSum = LegendBuilder.sum_color_counts(self.color_legend, 0)

        for color in self.color_legend:
            if "Color Hex" not in color or "Count" not in color:
                continue

            color_rgb_tuple = LegendBuilder.get_color_rgb_tuple(color["Color Hex"])

            if numeratorSum > 0:
                # Rectangle colored fraction width
                numeratorCount = LegendBuilder.get_legend_item_count(color, 0)  # [EXPD-2384]
                color_fraction = numeratorCount / numeratorSum  # [EXPD-2384]

                rectangle_portion_to_color = int(RECTANGLE_TOTAL_WIDTH * color_fraction)

                rectangle_tuple = (
                    self.rectangle_current_h_offset + self.rectangle_portion_colored,
                    self.rectangle_current_v_offset,
                    self.rectangle_current_h_offset + self.rectangle_portion_colored + rectangle_portion_to_color,
                    self.rectangle_current_v_offset + RECTANGLE_TOTAL_HEIGHT,
                )

                # Draw the colored rectangle portion
                self.PIL_legend_draw.rectangle(xy=rectangle_tuple, fill=color_rgb_tuple)

                self.rectangle_portion_colored += rectangle_portion_to_color

            # Create an Ink color
            tuple_color = tuple(
                int(color["Color Hex"][color_drawing_counter : color_drawing_counter + 2], 16)
                for color_drawing_counter in (0, 2, 4, 6)
            )

            self.PIL_legend_draw.ellipse(
                (
                    H_OFFSET_LEGEND_ITEMS,
                    self.current_v_pointer + LEGEND_ITEM_INTRA_OFFSET,
                    H_OFFSET_LEGEND_ITEMS + LEGEND_ITEM_CIRCLE_SIZE,
                    self.current_v_pointer + LEGEND_ITEM_INTRA_OFFSET + LEGEND_ITEM_CIRCLE_SIZE,
                ),
                fill=tuple_color,
                width=40,
            )

            self.PIL_legend_draw.text(
                xy=(H_OFFSET_LEGEND_ITEMS + LEGEND_ITEM_CIRCLE_SIZE + LEGEND_ITEM_INTRA_OFFSET, self.current_v_pointer),
                text=color["Category"] if "Category" in color else color["Range"],
                fill=WHITE_TEXT_RGB if self.dark_theme else GRAY_TEXT_RGB,
                font=self.PIL_item_font,
            )

            self.current_v_pointer += (
                LEGEND_ITEM_INTRA_OFFSET + LEGEND_ITEM_CIRCLE_SIZE + LEGEND_ITEM_INTRA_OFFSET + V_PADDING
            )

            color_drawing_counter += 1

    def draw_color_legend_gradient(self, gradient_type: GradientType):
        def draw_gradient_rectangle(width, height, start_color, end_color):
            image = Image.new("RGB", (width, height))
            draw = ImageDraw.Draw(image)

            for x in range(width):
                current_color = tuple(
                    int(start + (end - start) * x / width) for start, end in zip(start_color, end_color)
                )
                draw.line([(x, 0), (x, height)], fill=current_color)

            return image

        detail_min = self.color_legend[f"{gradient_type.value} Original Min"]
        detail_max = self.color_legend[f"{gradient_type.value} Original Max"]

        if "Color Hex Values" not in self.color_legend:
            self.color_legend["Color Hex Values"] = DEFAULT_COLOR_GRADIENT_HEX

        rectangle_gradient_hex = self.color_legend["Color Hex Values"].split(", ")
        rectangle_gradient_tickmarks = [LegendBuilder.get_color_rgb_tuple(color) for color in rectangle_gradient_hex]

        n_sections = len(rectangle_gradient_hex) - 1
        # Define the dimensions of the rectangle sections
        section_width = int(RECTANGLE_TOTAL_WIDTH / n_sections)
        for i in range(n_sections):
            gradient_rectangle_section = draw_gradient_rectangle(
                section_width,
                RECTANGLE_TOTAL_HEIGHT,
                rectangle_gradient_tickmarks[i],
                rectangle_gradient_tickmarks[i + 1],
            )
            self.PIL_legend_image.paste(
                gradient_rectangle_section,
                (self.rectangle_current_h_offset + self.rectangle_portion_colored, self.rectangle_current_v_offset),
            )

            self.rectangle_portion_colored += section_width

        self.PIL_legend_draw.text(
            xy=(
                H_OFFSET_LEGEND_ITEMS + H_OFFSET_ITEMS + LEGEND_ITEM_INTRA_OFFSET,
                self.current_v_pointer + TITLE_FONT_SIZE,
            ),
            text=detail_min,
            fill=DETAIL_TEXT_RGB,
            font=self.PIL_item_font,
            align="center",
            anchor="ms",
        )

        self.PIL_legend_draw.text(
            xy=(H_OFFSET_LEGEND_ITEMS * 6 + H_PADDING * SCALE_RATIO, self.current_v_pointer + TITLE_FONT_SIZE),
            text=detail_max,
            fill=DETAIL_TEXT_RGB,
            font=self.PIL_item_font,
            align="center",
            anchor="ms",
        )

        stat_item_v_offset = (
            LEGEND_ITEM_INTRA_OFFSET + LEGEND_ITEM_CIRCLE_SIZE + LEGEND_ITEM_INTRA_OFFSET + V_PADDING * 2
        )

        if gradient_type == GradientType.GRADIENT:
            stats = ["Count", "Min", "Max", "Med", "Avg", "STD", "Missing"]
            for stat in stats:
                self.current_v_pointer += stat_item_v_offset
                self.PIL_legend_draw.text(
                    xy=(H_OFFSET_LEGEND_ITEMS + LEGEND_ITEM_CIRCLE_SIZE, self.current_v_pointer),
                    text=stat + ": " + str(self.color_legend[stat]),
                    fill=WHITE_TEXT_RGB if self.dark_theme else GRAY_TEXT_RGB,
                    font=self.PIL_item_font,
                )
            self.current_v_pointer += stat_item_v_offset // 2
        else:
            self.current_v_pointer += RECTANGLE_TOTAL_HEIGHT * 2

    def draw_shape_legend(self):
        shape_legend = self.legend_dict["Shape"]

        # TODO: The title should be dynamic, maybe fetched from the plot method parameters
        self.PIL_legend_draw.text(
            (H_PADDING + H_OFFSET_ITEMS + 50, self.current_v_pointer),
            self.legend_dict["Shape Column"],
            fill=WHITE_TEXT_RGB if self.dark_theme else GRAY_TEXT_RGB,
            font=self.PIL_title_font,
        )

        with importlib.resources.path("virtualitics.assets", "shapes.png") as path:
            # Draw svg image
            shapes_icon = Image.open(str(path)).resize((H_OFFSET_ITEMS - 10, H_OFFSET_ITEMS))

            # Replace only black pixels with white ones
            shapes_icon = self.replace_color(shapes_icon, (0, 0, 0), self.bg_color)

            self.PIL_legend_image.paste(shapes_icon, (H_PADDING + 10, self.current_v_pointer))

        self.current_v_pointer += V_PADDING * 3
        shape_drawing_counter = 1
        for shape in shape_legend:
            with importlib.resources.path("virtualitics.assets", get_icon_name(shape)) as path:
                shape_icon = Image.open(str(path)).resize((LEGEND_ITEM_CIRCLE_SIZE, LEGEND_ITEM_CIRCLE_SIZE))

                # Replace only black pixels with white ones
                shape_icon = self.replace_color(shape_icon, (0, 0, 0), self.bg_color)
                self.PIL_legend_image.paste(
                    shape_icon,
                    (
                        H_OFFSET_LEGEND_ITEMS,
                        self.current_v_pointer + LEGEND_ITEM_INTRA_OFFSET,
                    ),
                )

            self.PIL_legend_draw.text(
                xy=(H_OFFSET_LEGEND_ITEMS + LEGEND_ITEM_CIRCLE_SIZE + LEGEND_ITEM_INTRA_OFFSET, self.current_v_pointer),
                text=shape["Category"] if "Category" in shape else shape["Range"],
                fill=WHITE_TEXT_RGB if self.dark_theme else GRAY_TEXT_RGB,
                font=self.PIL_item_font,
            )

            # Load all the assets in a dictionary

            self.current_v_pointer += (
                LEGEND_ITEM_INTRA_OFFSET + LEGEND_ITEM_CIRCLE_SIZE + LEGEND_ITEM_INTRA_OFFSET + V_PADDING
            )
            shape_drawing_counter += 1
