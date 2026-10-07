import os
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from yt_dlp import YoutubeDL

# ضبط ثيم الألوان ليصبح أزرق داكن فخم (Dark Blue Theme)
Window.clearcolor = (0.02, 0.05, 0.12, 1)

class SanemiDownloaderProApp(App):
    def build(self):
        root_layout = BoxLayout(orientation='vertical', padding=18, spacing=14)
        
        # قسم العنوان
        header_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=65, spacing=4)
        self.app_title = Label(
            text="⚡ SANEMI DOWNLOADER PRO ⚡",
            font_size='20sp',
            bold=True,
            color=(0.1, 0.6, 1, 1),
            halign='center'
        )
        self.app_subtitle = Label(
            text="المحرك الخارق للتحميل السريع والتحكم المطلق بالـ FPS",
            font_size='11sp',
            color=(0.5, 0.7, 0.9, 1),
            halign='center'
        )
        header_layout.add_widget(self.app_title)
        header_layout.add_widget(self.app_subtitle)
        root_layout.add_widget(header_layout)
        
        # حقل إدخال الرابط
        input_container = BoxLayout(orientation='vertical', size_hint_y=None, height=60, spacing=5)
        input_label = Label(text="رابط الفيديو (يوتيوب، انستغرام، تيك توك...):", font_size='12sp', color=(0.7, 0.8, 0.9, 1), halign='left')
        input_label.bind(size=input_label.setter('text_size'))
        
        self.url_input = TextInput(
            hint_text='https://www.youtube.com/watch?v=...',
            multiline=False,
            size_hint_y=None,
            height=40,
            background_color=(0.06, 0.1, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.35, 0.45, 0.6, 1),
            padding_x=12,
            cursor_color=(0.1, 0.6, 1, 1)
        )
        input_container.add_widget(input_label)
        input_container.add_widget(self.url_input)
        root_layout.add_widget(input_container)
        
        # خيارات الجودة والـ FPS
        options_layout = GridLayout(cols=2, size_hint_y=None, height=75, spacing=10)
        
        q_box = BoxLayout(orientation='vertical', spacing=3)
        q_label = Label(text="جودة الفيديو:", font_size='11sp', color=(0.7, 0.8, 0.9, 1), halign='left')
        q_label.bind(size=q_label.setter('text_size'))
        self.quality_spinner = Spinner(
            text='1080p (Full HD)',
            values=('2160p (4K Ultra)', '1080p (Full HD)', '720p (HD)', '480p (SD)', 'أفضل جودة متاحة'),
            background_color=(0.08, 0.18, 0.35, 1),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=40
        )
        q_box.add_widget(q_label)
        q_box.add_widget(self.quality_spinner)
        
        fps_box = BoxLayout(orientation='vertical', spacing=3)
        fps_label = Label(text="معدل الإطارات (FPS):", font_size='11sp', color=(0.7, 0.8, 0.9, 1), halign='left')
        fps_label.bind(size=fps_label.setter('text_size'))
        self.fps_spinner = Spinner(
            text='60fps (سلس جداً)',
            values=('60fps (سلس جداً)', '30fps (عادي/قياسي)', 'الافتراضي (Auto)'),
            background_color=(0.08, 0.18, 0.35, 1),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=40
        )
        fps_box.add_widget(fps_label)
        fps_box.add_widget(self.fps_spinner)
        
        options_layout.add_widget(q_box)
        options_layout.add_widget(fps_box)
        root_layout.add_widget(options_layout)
        
        root_layout.add_widget(Label(size_hint_y=None, height=5))
        
        # زر التحميل
        self.download_btn = Button(
            text='🚀 بدء التحميل الفائق (High Speed)',
            size_hint_y=None,
            height=55,
            background_color=(0.05, 0.4, 0.85, 1),
            background_normal='',
            bold=True,
            font_size='15sp'
        )
        self.download_btn.bind(on_press=self.on_download_click)
        root_layout.add_widget(self.download_btn)
        
        # شريط التقدم
        progress_container = BoxLayout(orientation='vertical', size_hint_y=None, height=45, spacing=4)
        self.progress_label = Label(text="حالة التحميل: 0%", font_size='11sp', color=(0.6, 0.8, 1, 1), halign='right')
        self.progress_label.bind(size=self.progress_label.setter('text_size'))
        
        self.progress_bar = ProgressBar(max=100, value=0, size_hint_y=None, height=20)
        progress_container.add_widget(self.progress_label)
        progress_container.add_widget(self.progress_bar)
        root_layout.add_widget(progress_container)
        
        # صندوق السجلات
        scroll_view = ScrollView(size_hint=(1, 1))
        self.log_label = Label(
            text="[ النظام جاهز للاستخدام... أدخل رابط الفيديو في الأعلى وأضف إعداداتك ]\n",
            font_size='12sp',
            color=(0.65, 0.85, 1, 1),
            valign='top',
            halign='left',
            size_hint_y=None
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        scroll_view.add_widget(self.log_label)
        root_layout.add_widget(scroll_view)
        
        return root_layout

    def log_message(self, message):
        print(message)
        self.log_label.text += f"\n{message}"

    def on_download_click(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.log_message("[!] تنبيه: يرجى إدخال رابط الفيديو المُراد تحميله أولاً.")
            return
        
        self.download_btn.disabled = True
        self.progress_bar.value = 5
        self.progress_label.text = "حالة التحميل: جاري الاتصال..."
        self.log_message(f"[*] تم رصد الرابط، جاري تهيئة محرك السحب...")
        
        threading.Thread(target=self.execute_download_engine, args=(url,)).start()

    def execute_download_engine(self, url):
        try:
            quality_choice = self.quality_spinner.text
            fps_choice = self.fps_spinner.text
            
            format_selector = 'bestvideo+bestaudio/best'
            if '2160p' in quality_choice:
                format_selector = 'bestvideo[height<=2160]+bestaudio/best'
            elif '1080p' in quality_choice:
                format_selector = 'bestvideo[height<=1080]+bestaudio/best'
            elif '720p' in quality_choice:
                format_selector = 'bestvideo[height<=720]+bestaudio/best'
            elif '480p' in quality_choice:
                format_selector = 'bestvideo[height<=480]+bestaudio/best'
                
            if '60fps' in fps_choice:
                format_selector += '[fps>=50]'
            elif '30fps' in fps_choice:
                format_selector += '[fps<50]'

            ydl_opts = {
                'format': format_selector,
                'outtmpl': '%(title)s [%(resolution)s].%(ext)s',
                'progress_hooks': [self.download_progress_hook],
                'noplaylist': True,
            }

            self.log_message(f"[*] بدء سحب الفيديو بجودة ({quality_choice}) ومعدل ({fps_choice})...")

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.progress_bar.value = 100
            self.progress_label.text = "حالة التحميل: 100% (مكتمل)"
            self.log_message("[✓] تم تحميل ومعالجة الفيديو وحفظه في جهازك بنجاح تام!")

        except Exception as err:
            self.log_message(f"[x] حدث خطأ تقني أثناء التحميل: {str(err)}")
            self.progress_label.text = "حالة التحميل: فشل"
        finally:
            self.download_btn.disabled = False

    def download_progress_hook(self, d):
        if d['status'] == 'downloading':
            try:
                p_str = d.get('_percent_str', '0%').replace('%', '').strip()
                p_val = float(p_str)
                self.progress_bar.value = p_val
                self.progress_label.text = f"حالة التحميل: {p_str}%"
            except Exception:
                pass

if __name__ == '__main__':
    SanemiDownloaderProApp().run()
