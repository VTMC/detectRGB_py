import os

import customtkinter as ctk
from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image, ImageTk

class ImageProcessingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.THRESH_MAX_VALUE = 255
        self.MAX_VALUE = 4000
        self.MIN_BLOCK_SIZE = 3
        self.THRESHOLD_TYPES = ["BINARY", "BINARY_INVERTED", "TRUNCATE", "TO_ZERO", "TO_ZERO_INVERTED"]
        self.THRESHOLD_OPTIONS = ["None","OTSU", "TRIANGLE"]
        self.ADAPTIVE_METHODS = ["MEAN_C", "GAUSSIAN_C"]
        self.TAB1_NAME = "Threshold"
        self.TAB2_NAME = "Adaptive Threshold"
        
        self.path = None
        self.read_fileName = None
        self.original_image = None
        self.processed_image = None
        
        self.zoom_scale = 0.1
        self.image_x = 0
        self.image_y = 0
        self.drag_x = 0
        self.drag_y = 0
        self.canvas_image_id = None
        
        self.threshold_value = 127
        self.threshold_type = cv2.THRESH_BINARY
        self.threshold_option = None
        self.adaptive_method = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
        self.adaptive_block_size = 11
        self.adaptive_C = 2
        
        # For UI
        self.geometry("800x1000")
        self.title("OpenCV Binary Test Program")
        
        # 이미지 선택 버튼 및 경로 입력 필드 표시
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.pack(
            padx=20,
            pady=(40, 10),
            fill="x"
        )
        
        self.path_label = ctk.CTkLabel(
            self.path_frame,
            text="이미지 파일을 선택하세요.",
            anchor="w"
        )
        self.path_label.grid(
            row=0,
            column=0,
            padx=(10, 5),
            pady=10,
            sticky="ew"
        )
        
        self.select_button = ctk.CTkButton(
            self.path_frame,
            text="Select Image",
            command=self.select_image
        )
        
        self.select_button.grid(row=0, column=1, padx=(5, 10), pady=10)
        self.path_frame.grid_columnconfigure(0, weight=1)
        
        # 이미지 처리 토글 버튼 적용
        self.mode_toggle = ctk.CTkSwitch(self, text="이미지 처리 적용", command=self.on_mode_toggle)
        self.mode_toggle.pack(pady=10, anchor="ne", padx=10)
        
        # 탭 뷰 추가
        self.tabView = ctk.CTkTabview(self)
        # self.tabView.pack(expand=True, fill="both")
        self.tabView.pack(
            padx=20,
            pady=10,
            fill="x",
            expand=False
        )
        
        # 탭 추가
        self.tab1 = self.tabView.add(self.TAB1_NAME)
        self.tab2 = self.tabView.add(self.TAB2_NAME)
        
        self.tab1_content()
        self.tab2_content()
        
        self.temp_frame_1 = ctk.CTkFrame(self)
        self.temp_frame_1.pack(
            padx=20,
            pady=(40, 10),
            fill="x"
        )

        # 이미지 저장 버튼
        self.save_button = ctk.CTkButton(
            self.temp_frame_1,
            text="Save Image",
            command=self.save_image,
            state="disabled"
        )
        self.save_button.grid(row=0,column=1,padx=5,pady=10,sticky="ew")
        
        self.gaussianBlurCheckbox = ctk.CTkCheckBox(
            self.temp_frame_1,
            text="Gaussian Blur Apply",
            command=self.on_mode_toggle
        )
        self.gaussianBlurCheckbox.grid(row=0,column=0,padx=5,pady=10,sticky="ew")
        
        self.temp_frame_1.columnconfigure(0, weight=1)
        self.temp_frame_1.columnconfigure(1, weight=1)
        
        # 이미지 표시 영역
        self.image_label = ctk.CTkLabel(
            self,
            text="이미지 없음",
            fg_color=("gray85","gray20")
        )
        self.image_label.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.image_canvas = ctk.CTkCanvas(
            self,
            background="gray85",
            highlightthickness=0,
        )
        
        self.image_canvas.pack_forget() #UI 숨김 (Pack - Invisible)
        
        # self.image_canvas.pack(padx=20, pady=10, fill="both", expand=True) #UI 그릴 때 사용 (Pack - Visible)
        
        """+ａ
        # 숨기기
        self.widget.grid_remove()

        # 원래 위치에 다시 표시
        self.widget.grid()
        """
        
        self.image_canvas.bind("<ButtonPress-1>", self.start_drag)
        self.image_canvas.bind("<B1-Motion>", self.drag_image)
        self.image_canvas.bind("<MouseWheel>", self.zoom_image)
        
        
        
    def tab1_content(self):
        # Threshold 임계값 선택 가능한 프레임
        self.tab1_slider_frame = ctk.CTkFrame(self.tab1)
        self.tab1_slider_frame.pack(
                padx=10,
                pady=10,
                fill="x"
            )
        
        self.tab1_threshold_value_label = ctk.CTkLabel(self.tab1_slider_frame, text="Thresh", font=("Arial", 25, "bold"))
        self.tab1_threshold_value_label.grid(row=0,column=0,padx=5,pady=10,sticky="ew")
        
        self.tab1_threshold_value_slider = ctk.CTkSlider(
            self.tab1_slider_frame,
            from_=0,
            to=self.THRESH_MAX_VALUE,
            command=lambda value: self.set_threshold_value(
                    value,
                    self.tab1,
                    self.tab1_threshold_value_slider
                )
        )
        self.tab1_threshold_value_slider.grid(row=0,column=1,padx=5,pady=10,sticky="ew")
        
        self.tab1_show_threshold_value_entry = ctk.CTkEntry(
            self.tab1_slider_frame, 
            font=("Arial", 18)
        )
        self.tab1_show_threshold_value_entry.grid(row=0,column=2,padx=5,pady=10,sticky="ew")
        self.tab1_show_threshold_value_entry.bind(
            "<Return>", 
            lambda event: self.set_threshold_value(
                self.tab1_show_threshold_value_entry.get(),
                self.tab1,
                self.tab1_show_threshold_value_entry
            )
        )
        self.tab1_show_threshold_value_entry.insert(0, "127")
        
        self.tab1_slider_frame.grid_columnconfigure(0, weight=1)
        self.tab1_slider_frame.grid_columnconfigure(1, weight=3)
        self.tab1_slider_frame.grid_columnconfigure(2, weight=1)

        # Threshold Type 선택 가능한 프레임
        self.tab1_type_frame = ctk.CTkFrame(self.tab1)
        self.tab1_type_frame.pack(
                        padx=10,
                        pady=10,
                        fill="x"
                    )
        
        self.tab1_threshold_type_label = ctk.CTkLabel(self.tab1_type_frame, text="Type", font=("Arial", 25, "bold"))
        self.tab1_threshold_type_label.grid(row=0,column=0,padx=5,pady=10,sticky="ew")
        
        self.tab1_combobox_threshold_type = ctk.CTkComboBox(self.tab1_type_frame, values=self.THRESHOLD_TYPES,
                                                            command=lambda value: self.set_threshold_value(
                                                                value,
                                                                self.tab1,
                                                                self.tab1_combobox_threshold_type
                                                            ))
        self.tab1_combobox_threshold_type.grid(row=0,column=1,padx=5,pady=10,sticky="ew")
        
        self.tab1_combobox_threshold_option = ctk.CTkComboBox(self.tab1_type_frame, values=self.THRESHOLD_OPTIONS,
                                                              command=lambda value: self.set_threshold_value(
                                                                value,
                                                                self.tab1,
                                                                self.tab1_combobox_threshold_option
                                                            ))
        self.tab1_combobox_threshold_option.grid(row=0,column=2,padx=5,pady=10,sticky="ew")
        
        self.tab1_type_frame.grid_columnconfigure(0, weight=1)
        self.tab1_type_frame.grid_columnconfigure(1, weight=2)
        self.tab1_type_frame.grid_columnconfigure(2, weight=2)
        

    def tab2_content(self):
        # Threshold Type 선택 가능한 프레임
        self.tab2_type_frame = ctk.CTkFrame(self.tab2)
        self.tab2_type_frame.pack(
                        padx=10,
                        pady=10,
                        fill="x"
                    )
        
        self.tab2_method_type_title = ctk.CTkLabel(self.tab2_type_frame, text="AdaptiveMethod / Type", font=("Arial", 25, "bold"))
        self.tab2_method_type_title.grid(row=0,column=0,padx=5,pady=10,sticky="ew")
        
        self.tab2_combobox_adaptive_method = ctk.CTkComboBox(
            self.tab2_type_frame, 
            values=self.ADAPTIVE_METHODS,
            command=lambda value: self.set_threshold_value(
                value,
                self.tab2,
                self.tab2_combobox_adaptive_method
            )
        )
        self.tab2_combobox_adaptive_method.grid(row=0,column=1,padx=5,pady=10,sticky="ew")
        
        self.tab2_combobox_threshold_type = ctk.CTkComboBox(
            self.tab2_type_frame, 
            values=self.THRESHOLD_TYPES,
            command=lambda value: self.set_threshold_value(
                value,
                self.tab2,
                self.tab2_combobox_threshold_type
            )
        )
        self.tab2_combobox_threshold_type.grid(row=0,column=2,padx=5,pady=10,sticky="ew")
        
        self.tab2_type_frame.grid_columnconfigure(0, weight=1)
        self.tab2_type_frame.grid_columnconfigure(1, weight=2)
        self.tab2_type_frame.grid_columnconfigure(2, weight=2)

        # Threshold 임계값 선택 가능한 프레임
        self.tab2_slider_frame = ctk.CTkFrame(self.tab2)
        self.tab2_slider_frame.pack(
                padx=10,
                pady=10,
                fill="x"
            )
        
        # Adaptive Threshold Blocksize
        self.tab2_blocksize_value_label = ctk.CTkLabel(self.tab2_slider_frame, text="Blocksize", font=("Arial", 25, "bold"))
        self.tab2_blocksize_value_label.grid(row=0,column=0,padx=5,pady=10,sticky="ew")
        
        self.tab2_blocksize_value_slider = ctk.CTkSlider(
            self.tab2_slider_frame,
            from_=self.MIN_BLOCK_SIZE,
            to=self.MAX_VALUE,
            command=lambda value: self.set_threshold_value(
                    value,
                    self.tab2,
                    self.tab2_blocksize_value_slider
                )
        )
        self.tab2_blocksize_value_slider.grid(row=0,column=1,padx=5,pady=10,sticky="ew")
        
        self.tab2_show_blocksize_value_entry = ctk.CTkEntry(
            self.tab2_slider_frame, 
            font=("Arial", 18)
        )
        self.tab2_show_blocksize_value_entry.grid(row=0,column=2,padx=5,pady=10,sticky="ew")
        self.tab2_show_blocksize_value_entry.bind(
            "<Return>", 
            lambda event: self.set_threshold_value(
                self.tab2_show_blocksize_value_entry.get(),
                self.tab2,
                self.tab2_show_blocksize_value_entry
            )
        )
        self.tab2_show_blocksize_value_entry.insert(0, "3")
        
        # Adaptive Threshold C Value
        self.tab2_c_value_label = ctk.CTkLabel(self.tab2_slider_frame, text="C Value", font=("Arial", 25, "bold"))
        self.tab2_c_value_label.grid(row=1,column=0,padx=5,pady=10,sticky="ew")
        
        self.tab2_c_value_slider = ctk.CTkSlider(
            self.tab2_slider_frame,
            from_=-self.MAX_VALUE,
            to=self.MAX_VALUE,
            command=lambda value: self.set_threshold_value(
                    value,
                    self.tab2,
                    self.tab2_c_value_slider
                )
        )
        self.tab2_c_value_slider.grid(row=1,column=1,padx=5,pady=10,sticky="ew")
        
        self.tab2_show_c_value_entry = ctk.CTkEntry(
            self.tab2_slider_frame, 
            font=("Arial", 18)
        )
        self.tab2_show_c_value_entry.grid(row=1,column=2,padx=5,pady=10,sticky="ew")
        self.tab2_show_c_value_entry.bind(
            "<Return>", 
            lambda event: self.set_threshold_value(
                self.tab2_show_c_value_entry.get(),
                self.tab2,
                self.tab2_show_c_value_entry
            )
        )
        self.tab2_show_c_value_entry.insert(0, "0")
        
        self.tab2_slider_frame.grid_columnconfigure(0, weight=1)
        self.tab2_slider_frame.grid_columnconfigure(1, weight=3)
        self.tab2_slider_frame.grid_columnconfigure(2, weight=1)
        
    def set_threshold_value(self, value, tab_type, ui_type):
        """ threshold의 value값을 설정합니다. """
        
        try:
            inputted_value = int(float(value))
        except ValueError:
            inputted_value = value

        if tab_type is self.tab1:
            match ui_type:
                case self.tab1_show_threshold_value_entry | self.tab1_threshold_value_slider:
                    # 0~255 범위로 제한
                    inputted_value = max(0, min(self.THRESH_MAX_VALUE, inputted_value))
                    
                    self.tab1_show_threshold_value_entry.delete(0, ctk.END)
                    self.tab1_show_threshold_value_entry.insert(0, str(inputted_value))
                    self.tab1_threshold_value_slider.set(inputted_value)
                    
                    self.threshold_value = inputted_value
                    
                case self.tab1_combobox_threshold_type:
                    if inputted_value in self.THRESHOLD_TYPES:
                        match inputted_value:
                            case "BINARY_INVERTED":
                                self.threshold_type = cv2.THRESH_BINARY_INV
                            case "TRUNCATE":
                                self.threshold_type = cv2.THRESH_TRUNC
                            case "TO_ZERO":
                                self.threshold_type = cv2.THRESH_TOZERO
                            case "TO_ZERO_INVERSE":
                                self.threshold_type = cv2.THRESH_TOZERO_INV
                            case "BINARY" | _:
                                self.threshold_type = cv2.THRESH_BINARY
                                
                        print("threshold type set to : ", inputted_value)
                                
                case self.tab1_combobox_threshold_option:
                    if inputted_value in self.THRESHOLD_OPTIONS:
                        match inputted_value:
                            case "OTSU":
                                self.threshold_option = cv2.THRESH_OTSU
                            case "TRIANGLE":
                                self.threshold_option = cv2.THRESH_TRIANGLE
                            case _:
                                self.threshold_option = None
                    
                    print("threshold option set to : ", inputted_value) 
            
            
        
        elif tab_type is self.tab2:
            match ui_type:
                case self.tab2_show_blocksize_value_entry | self.tab2_blocksize_value_slider:
                    # 3~9999 범위로 제한
                    inputted_value = max(self.MIN_BLOCK_SIZE, min(self.MAX_VALUE, inputted_value))
                    
                    if inputted_value % 2 == 0:
                        inputted_value += 1
                    
                    self.tab2_show_blocksize_value_entry.delete(0, ctk.END)
                    self.tab2_show_blocksize_value_entry.insert(0, str(inputted_value))
                    self.tab2_blocksize_value_slider.set(inputted_value)
                    
                    self.adaptive_block_size = inputted_value
                    
                case self.tab2_show_c_value_entry | self.tab2_c_value_slider:
                    # -9999~9999 범위로 제한
                    inputted_value = max(-self.MAX_VALUE, min(self.MAX_VALUE, inputted_value))
                    
                    self.tab2_show_c_value_entry.delete(0, ctk.END)
                    self.tab2_show_c_value_entry.insert(0, str(inputted_value))
                    self.tab2_c_value_slider.set(inputted_value)
                    
                    self.adaptive_C = inputted_value
                    
                case self.tab2_combobox_adaptive_method:
                    if inputted_value in self.ADAPTIVE_METHODS:
                        match inputted_value:
                            case "GAUSSIAN_C":
                                self.threshold_type = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
                            case "MEAN_C" | _:
                                self.threshold_type = cv2.ADAPTIVE_THRESH_MEAN_C
                                
                        print("threshold type set to : ", inputted_value)
                        
                        
                case self.tab2_combobox_threshold_type:
                    if inputted_value in self.THRESHOLD_TYPES:
                        match inputted_value:
                            case "BINARY_INVERTED":
                                self.threshold_type = cv2.THRESH_BINARY_INV
                            case "TRUNCATE":
                                self.threshold_type = cv2.THRESH_TRUNC
                            case "TO_ZERO":
                                self.threshold_type = cv2.THRESH_TOZERO
                            case "TO_ZERO_INVERSE":
                                self.threshold_type = cv2.THRESH_TOZERO_INV
                            case "BINARY" | _:
                                self.threshold_type = cv2.THRESH_BINARY
                                
                        print("threshold type set to : ", inputted_value)
                        
                        
        print("Adaptive threshold option set to : ", inputted_value)
        
        # 이미지 처리 여부를 진행
        self.on_mode_toggle()
                
    def on_mode_toggle(self):
        selected_tab = self.tabView.get()
        toggle_value = self.mode_toggle.get()
        
        if toggle_value == 1:
            if selected_tab == self.TAB1_NAME:
                self.threshold_image(self.tab1)
            elif selected_tab == self.TAB2_NAME:
                self.threshold_image(self.tab2)
        else:
            self.show_image(self.original_image)
            
    def select_image(self):
        selected_path = filedialog.askopenfilename(
            title="이미지 파일 선택",
            filetypes=[
                (
                    "Image Files",
                    "*.jpg *.jpeg *.png *.bmp *.webp *.tif *.tiff"
                ),
                ("JPEG Files", "*.jpg *.jpeg"),
                ("PNG Files", "*.png"),
                ("All Files", "*.*")
            ]
        )
        
        # 사용자가 취소하면 빈 문자열이 반환됨
        if not selected_path:
            return
        
        self.path = selected_path
        self.read_fileName = os.path.splitext(os.path.basename(self.path))[0]
        self.path_label.configure(text=self.path)

        print("선택된 이미지:", self.path)
        
        self.original_image = self.read_image(self.path)
        
        if self.original_image is None:
            self.image_canvas.pack_forget()
            self.image_label.pack(padx=20, pady=10, fill="both", expand=True)
            
            self.image_label.configure(text="이미지를 읽을 수 없습니다.", image=None)
            return

        self.show_image(self.original_image)
        print("선택된 이미지:", self.path)
        print("이미지 크기:", self.original_image.shape)
        
    def read_image(self, image_path):
        """
        한글 경로를 포함한 이미지도 읽을 수 있도록
        np.fromfile과 cv2.imdecode를 사용합니다.
        """
        try:
            image_data = np.fromfile(
                image_path,
                dtype=np.uint8
            )
            
            cv_image_data =  cv2.imdecode(
                image_data,
                cv2.IMREAD_COLOR
            )
            
            # OpenCV BGR -> RGB
            rgb_image = cv2.cvtColor(cv_image_data, cv2.COLOR_BGR2RGB)
            
            return rgb_image
            
        except Exception as e:
            print("이미지 읽기 오류 : ",e)
            return None
        
    def threshold_image(self, tab_type):
        """
        읽어온 이미지를 threshold 및 adaptive threshold로 처리하기 위한 함수입니다.
        """
        
        if(self.original_image is None):
            self.image_canvas.pack_forget()
            self.image_label.pack(padx=20, pady=10, fill="both", expand=True)
            
            self.image_label.configure(text="읽어온 이미지가 없습니다.", image=None)
            return
        
        gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        
        if self.gaussianBlurCheckbox.get() == 1:
            gray_image = cv2.GaussianBlur(
                gray_image,
                (5, 5),
                0
            )
        
        if tab_type == self.tab1: #threshold
            ret, self.processed_image = cv2.threshold(
                gray_image,
                self.tab1_threshold_value_slider.get(),
                self.THRESH_MAX_VALUE,
                self.threshold_type,
            )
            
            if ret:
                self.show_image(self.processed_image)
            else:
                self.processed_image = None
                self.image_canvas.pack_forget()
                self.image_label.pack(padx=20, pady=10, fill="both", expand=True)
                
                self.image_label.configure(text="Threshold 처리에 실패했습니다.", image=None)
            
            
        elif tab_type == self.tab2: # adaptive threshold
            self.processed_image = cv2.adaptiveThreshold(
                gray_image,
                self.THRESH_MAX_VALUE,
                self.adaptive_method,
                self.threshold_type,
                self.adaptive_block_size,
                self.adaptive_C
            )
            
            if self.processed_image is not None:
                self.show_image(self.processed_image)
            else:
                self.processed_image = None
                self.image_canvas.pack_forget()
                self.image_label.pack(padx=20, pady=10, fill="both", expand=True)
                
                self.image_label.configure(text="Adaptive Threshold 처리에 실패했습니다.", image=None)
        
    def show_image(self, cv_image):
        """
        OpenCV BGR 이미지를 CustomTkinter에 표시합니다.
        """
        self.displayed_image = cv_image.copy()
        
        self.pil_image = Image.fromarray(cv_image)
        
        # 원본 비율을 유지하면서 최대 크기 계산
        # display_width, display_height = self.calculate_display_size(
        #     self.pil_image.width,
        #     self.pil_image.height,
        #     max_width=600,
        #     max_height=300
        # )

        # self.processed_image = ctk.CTkImage(
        #     light_image=self.pil_image,
        #     dark_image=self.pil_image,
        #     size=(display_width, display_height)
        # )

        self.image_label.pack_forget()
        self.image_canvas.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.draw_canvas_image()
        
        self.save_button.configure(state="normal")

    def calculate_display_size(
        self,
        image_width,
        image_height,
        max_width,
        max_height
    ):
        """
        이미지의 종횡비를 유지하면서 표시 크기를 계산합니다.
        """
        width_ratio = max_width / image_width
        height_ratio = max_height / image_height

        scale_ratio = min(
            width_ratio,
            height_ratio,
            1.0
        )

        display_width = int(image_width * scale_ratio)
        display_height = int(image_height * scale_ratio)

        return display_width, display_height
            
    def save_image(self):
        if not hasattr(self, "displayed_image"):
            return
        
        fileName = self.read_fileName
        
        fileName += "_ProcessedImage" if self.mode_toggle.get() == 1 else "_NotProcessedImage"
        
        if self.mode_toggle.get() == 1:
            if self.tabView.get() == self.TAB1_NAME:        
                fileName += "_Threshold"
                fileName += "_Value_"+str(self.threshold_value)
                fileName += "_Type_"+str(self.threshold_type)
                fileName += "_Option_"+str(self.threshold_option)
                
            else:
                fileName += "_AdaptiveThreshold"
                fileName += "_AdaptiveMethod_"+str(self.adaptive_method)
                fileName += "_Type_"+str(self.threshold_type)
                fileName += "_BlockSize_"+str(self.adaptive_block_size)
                fileName += "_C_"+str(self.adaptive_C)
                
            if self.gaussianBlurCheckbox.get() == 1:
                fileName += "_AddGaussianBlur"

        save_path = filedialog.asksaveasfilename(
            title="이미지 저장",
            initialfile=fileName,
            defaultextension=".png",
            filetypes=[
                ("PNG Files", "*.png"),
                ("JPEG Files", "*.jpg *.jpeg"),
                ("Bitmap Files", "*.bmp")
            ]
        )

        if not save_path:
            return

        save_image = self.displayed_image

        # 현재 컬러 이미지가 RGB이므로 OpenCV 저장 전에 BGR로 변환
        if len(save_image.shape) == 3:
            save_image = cv2.cvtColor(
                save_image,
                cv2.COLOR_RGB2BGR
            )

        extension = "." + save_path.split(".")[-1]

        success, encoded_image = cv2.imencode(
            extension,
            save_image
        )

        if success:
            encoded_image.tofile(save_path)
            print("이미지 저장 완료:", save_path)
        else:
            print("이미지 저장 실패")
            
    # 캔버스 이미지 다루는 함수 모임
    def draw_canvas_image(self):
        image_width = max(1, int(self.pil_image.width * self.zoom_scale))
        
        image_height = max(1, int(self.pil_image.height * self.zoom_scale))
        
        resized_image = self.pil_image.resize(
            (image_width, image_height),
            Image.Resampling.LANCZOS
        )
        
        self.canvas_photo = ImageTk.PhotoImage(resized_image)
        
        # 캔버스 크기 계산
        self.image_canvas.update_idletasks()
        
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()
        
        if self.canvas_image_id is None:
            # self.image_scale = 0.1
            self.image_x = (canvas_width - image_width) / 2
            self.image_y = (canvas_height - image_height) / 2
            
            self.canvas_image_id = self.image_canvas.create_image(
                self.image_x,
                self.image_y,
                anchor="nw",
                image=self.canvas_photo
            )
        else:
            self.image_canvas.itemconfig(
                self.canvas_image_id,
                image=self.canvas_photo
            )
            
            self.image_canvas.coords(
                self.canvas_image_id,
                self.image_x,
                self.image_y
            )
            
    def start_drag(self, event):
        self.drag_x = self.image_canvas.canvasx(event.x)
        self.drag_y = self.image_canvas.canvasy(event.y)
        
    def drag_image(self, event):
        if self.canvas_image_id is None:
            return
        
        print("drag:", event.x, event.y)
        
        current_x = self.image_canvas.canvasx(event.x)
        current_y = self.image_canvas.canvasy(event.y)
        
        move_x = current_x - self.drag_x
        move_y = current_y - self.drag_y
        
        self.image_canvas.move(
            self.canvas_image_id,
            move_x,
            move_y
        )
        
        self.image_x += move_x
        self.image_y += move_y
        
        self.drag_x = current_x
        self.drag_y = current_y
        
    def zoom_image(self, event):
        if not hasattr(self, "pil_image"):
            return
        
        old_scale = self.zoom_scale
        
        if event.delta > 0:
            self.zoom_scale *= 1.1
        else:
            self.zoom_scale /= 1.1
            
        self.zoom_scale = max(0.1, min(10.0, self.zoom_scale))
        
        print("zoom:", self.zoom_scale)
        
        scale_change = self.zoom_scale / old_scale
        
        # 마우스 위치 중심으로 확대, 축소
        self.image_x = event.x - (event.x - self.image_x) * scale_change
        self.image_y = event.y - (event.y - self.image_y) * scale_change

        self.draw_canvas_image()

# 기본 설정
ctk.set_appearance_mode("System")  # 시스템 모드 사용
ctk.set_default_color_theme("blue")  # 기본 색상 테마 설정

# 실행
app = ImageProcessingApp()
app.mainloop()  # 메인 루프 실행