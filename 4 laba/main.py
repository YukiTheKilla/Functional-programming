from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk, ImageFilter, ImageOps, ImageEnhance
import threading

class ImageProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        self.input_path = None
        self.original_image = None
        self.processed_image = None
        self.output_path = None

        # Start parameters
        self.sepia_intensity = DoubleVar(value=0.0)
        self.blur_radius = DoubleVar(value=1.0)
        self.sharpness_factor = DoubleVar(value=0.0)
        self.brightness = DoubleVar(value=1.0)
        self.resize_factor = DoubleVar(value=1.0)

        self.create_widgets()

    def create_widgets(self):
        select_button = Button(self.root, text="Select Image", command=self.select_image)
        select_button.pack(pady=10)

        sepia_label = Label(self.root, text="Sepia Intensity")
        sepia_label.pack()
        sepia_slider = Scale(self.root, from_=-5, to=5, variable=self.sepia_intensity, orient=HORIZONTAL, length=200, command=self.update_image)
        sepia_slider.pack()

        blur_label = Label(self.root, text="Blur Radius")
        blur_label.pack()
        blur_slider = Scale(self.root, from_=-5, to=5, variable=self.blur_radius, orient=HORIZONTAL, length=200, command=self.update_image)
        blur_slider.pack()

        sharpness_label = Label(self.root, text="Sharpness Factor")
        sharpness_label.pack()
        sharpness_slider = Scale(self.root, from_=-5, to=5, variable=self.sharpness_factor, orient=HORIZONTAL, length=200, command=self.update_image)
        sharpness_slider.pack()

        brightness_label = Label(self.root, text="Brightness")
        brightness_label.pack()
        brightness_slider = Scale(self.root, from_=0.1, to=2.0, resolution=0.1, variable=self.brightness, orient=HORIZONTAL, length=200, command=self.update_image)
        brightness_slider.pack()
        
        resize_label = Label(self.root, text="Resize Factor")
        resize_label.pack()
        resize_slider = Scale(self.root, from_=0.1, to=2.0, resolution=0.1, variable=self.resize_factor, orient=HORIZONTAL, length=200, command=self.update_image)
        resize_slider.pack()
        
        save_button = Button(self.root, text="Save Image", command=self.save_image)
        save_button.pack(pady=10)

        self.processed_image_label = Label(self.root)
        self.processed_image_label.pack()


    def select_image(self):
        self.input_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        if self.input_path:
            self.original_image = Image.open(self.input_path)

            self.display_image(self.original_image, self.processed_image_label)

    def update_image(self, *args):
        if self.input_path:
            self.processed_image = self.original_image.copy()

            processing_thread = threading.Thread(target=self.process_image)
            processing_thread.start()

    def process_image(self):
        sepia_intensity = int(self.sepia_intensity.get())
        sepia_image = ImageOps.colorize(self.processed_image.convert('L'), "#704214", "#C0A080")
        self.processed_image = Image.blend(self.processed_image, sepia_image, sepia_intensity)

        blur_radius = int(self.blur_radius.get())
        self.processed_image = self.processed_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

        sharpness_factor = float(self.sharpness_factor.get())
        sharpness = ImageEnhance.Sharpness(self.processed_image)
        self.processed_image = sharpness.enhance(sharpness_factor)

        resize_factor = float(self.resize_factor.get())
        new_width = int(self.original_image.width * resize_factor)
        new_height = int(self.original_image.height * resize_factor)
        self.processed_image = self.processed_image.resize((new_width, new_height))

        brightness_factor = float(self.brightness.get())
        self.processed_image = ImageEnhance.Brightness(self.processed_image).enhance(brightness_factor)

        self.display_image(self.processed_image, self.processed_image_label)

    def save_image(self):
        if self.processed_image:
            self.output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")], title="Save As")

            if self.output_path:
                format = "JPEG" if self.output_path.lower().endswith(".jpg") else "PNG"

                self.processed_image.save(self.output_path, format=format)

    def display_image(self, image, label):
        resize_factor = float(self.resize_factor.get())
        display_width = int(self.original_image.width * resize_factor)
        display_height = int(self.original_image.height * resize_factor)
        image = image.resize((display_width, display_height), Image.ANTIALIAS)

        tk_image = ImageTk.PhotoImage(image)

        label.config(image=tk_image, width=display_width, height=display_height)
        label.image = tk_image

if __name__ == "__main__":
    root = Tk()
    app = ImageProcessor(root)
    root.mainloop()
