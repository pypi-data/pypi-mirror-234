#!/usr/bin/env python3
import os
import io
from multiprocessing.queues import Queue as QueueType
from typing import Optional, Union

import imageio.v3 as iio
from rlottie_python import LottieAnimation # type: ignore
from apngasm_python._apngasm_python import APNGAsm, create_frame_from_rgba
import numpy as np
from PIL import Image
import av # type: ignore
from av.codec.context import CodecContext # type: ignore
import webp # type: ignore
import oxipng

from .codec_info import CodecInfo # type: ignore
from .cache_store import CacheStore # type: ignore
from .format_verify import FormatVerify # type: ignore
from .fake_cb_msg import FakeCbMsg # type: ignore

def get_step_value(max: int, min: int, step: int, steps: int) -> Optional[int]:
    if max and min:
        return round((max - min) * step / steps + min)
    else:
        return None

class StickerConvert:
    def __init__(self, in_f: Union[str, list[str, io.BytesIO]], out_f: str, opt_comp: dict, cb_msg=print):
        if type(cb_msg) != QueueType:
            cb_msg = FakeCbMsg(cb_msg)

        if type(in_f) == str:
            self.in_f = in_f
            self.in_f_name = os.path.split(self.in_f)[1]
            self.in_f_ext = CodecInfo.get_file_ext(self.in_f)
        else:
            self.in_f = in_f[1]
            self.in_f_name = os.path.split(in_f[0])[1]
            self.in_f_ext = CodecInfo.get_file_ext(in_f[0])

        self.out_f = out_f
        self.out_f_name = os.path.split(self.out_f)[1]
        if os.path.splitext(out_f)[0] not in ('null', 'bytes'):
            self.out_f_ext = CodecInfo.get_file_ext(self.out_f)
        else:
            self.out_f_ext = os.path.splitext(out_f)[1]

        self.cb_msg = cb_msg
        self.frames_raw: list[np.ndarray] = []
        self.frames_processed: list[np.ndarray] = []
        self.opt_comp = opt_comp
        self.preset = opt_comp.get('preset')

        self.size_max = opt_comp.get('size_max') if type(opt_comp.get('size_max')) == int else None
        self.size_max_img = opt_comp.get('size_max', {}).get('img') if not self.size_max else self.size_max
        self.size_max_vid = opt_comp.get('size_max', {}).get('vid') if not self.size_max else self.size_max

        self.format = opt_comp.get('format') if type(opt_comp.get('format')) == str else None
        self.format_img = opt_comp.get('format', {}).get('img') if not self.format else self.format
        self.format_vid = opt_comp.get('format', {}).get('vid') if not self.format else self.format

        self.fps = opt_comp.get('fps') if type(opt_comp.get('fps')) == int else None
        self.fps_min = opt_comp.get('fps', {}).get('min') if not self.fps else self.fps
        self.fps_max = opt_comp.get('fps', {}).get('max') if not self.fps else self.fps

        self.res_w = opt_comp.get('res', {}).get('w') if type(opt_comp.get('res', {}).get('w')) == int else None
        self.res_w_min = opt_comp.get('res', {}).get('w', {}).get('min') if not self.res_w else self.res_w
        self.res_w_max = opt_comp.get('res', {}).get('w', {}).get('max') if not self.res_w else self.res_w

        self.res_h = opt_comp.get('res', {}).get('h') if type(opt_comp.get('res', {}).get('h')) == int else None
        self.res_h_min = opt_comp.get('res', {}).get('h', {}).get('min') if not self.res_h else self.res_h
        self.res_h_max = opt_comp.get('res', {}).get('h', {}).get('max') if not self.res_h else self.res_h

        self.quality = opt_comp.get('quality') if type(opt_comp.get('quality')) == int else None
        self.quality_min = opt_comp.get('quality', {}).get('min') if not self.quality else self.quality
        self.quality_max = opt_comp.get('quality', {}).get('max') if not self.quality else self.quality

        self.color = opt_comp.get('color') if type(opt_comp.get('color')) == int else None
        self.color_min = opt_comp.get('color', {}).get('min') if not self.color else self.color
        self.color_max = opt_comp.get('color', {}).get('max') if not self.color else self.color

        self.duration = opt_comp.get('duration') if type(opt_comp.get('duration')) == int else None
        self.duration_min = opt_comp.get('duration', {}).get('min') if not self.duration else self.duration
        self.duration_max = opt_comp.get('duration', {}).get('max') if not self.duration else self.duration

        if not self.size_max and not self.size_max_img and not self.size_max_vid:
            self.steps = 1
        else:
            self.steps = opt_comp.get('steps') if opt_comp.get('steps') else 1
        self.fake_vid = opt_comp.get('fake_vid')
        self.cache_dir = opt_comp.get('cache_dir')

        self.tmp_f = None
        self.tmp_fs: list[bytes] = []

        self.apngasm = APNGAsm() # type: ignore[call-arg]

    def convert(self) -> tuple[bool, str, Union[None, bytes, str], int]:
        if (FormatVerify.check_format(self.in_f, format=self.out_f_ext) and
            FormatVerify.check_file_res(self.in_f, res=self.opt_comp.get('res')) and
            FormatVerify.check_file_fps(self.in_f, fps=self.opt_comp.get('fps')) and
            FormatVerify.check_file_size(self.in_f, size=self.opt_comp.get('size_max')) and
            FormatVerify.check_duration(self.in_f, duration=self.opt_comp.get('duration'))):
            self.cb_msg.put(f'[S] Compatible file found, skip compress and just copy {self.in_f_name} -> {self.out_f_name}')

            with open(self.in_f, 'rb') as f:
                self.write_out(f.read())
            return True, self.in_f, self.out_f, os.path.getsize(self.in_f)

        self.cb_msg.put(f'[I] Start compressing {self.in_f_name} -> {self.out_f_name}')

        steps_list = []
        for step in range(self.steps, -1, -1):
            steps_list.append((
                get_step_value(self.res_w_max, self.res_w_min, step, self.steps),
                get_step_value(self.res_h_max, self.res_h_min, step, self.steps),
                get_step_value(self.quality_max, self.quality_min, step, self.steps),
                get_step_value(self.fps_max, self.fps_min, step, self.steps),
                get_step_value(self.color_max, self.color_min, step, self.steps)
            ))
        self.tmp_fs = [None] * (self.steps + 1)

        step_lower = 0
        step_upper = self.steps

        if self.size_max_vid == None and self.size_max_img == None:
            # No limit to size, create the best quality result
            step_current = 0
        else:
            step_current = round((step_lower + step_upper) / 2)

        self.frames_import()
        while True:
            param = steps_list[step_current]
            self.res_w = param[0]
            self.res_h = param[1]
            self.quality = param[2]
            self.fps = param[3]
            self.color = param[4]

            self.tmp_f = io.BytesIO()
            self.cb_msg.put(f'[C] Compressing {self.in_f_name} -> {self.out_f_name} res={self.res_w}x{self.res_h}, quality={self.quality}, fps={self.fps}, color={self.color} (step {step_lower}-{step_current}-{step_upper})')
            
            self.frames_processed = self.frames_drop(self.frames_raw)
            self.frames_processed = self.frames_resize(self.frames_processed)
            self.frames_export()

            self.tmp_f.seek(0)
            size = self.tmp_f.getbuffer().nbytes
            if CodecInfo.is_anim(self.in_f):
                size_max = self.size_max_vid
            else:
                size_max = self.size_max_img
            
            if not size_max or size < size_max:
                self.tmp_fs[step_current] = self.tmp_f.read()

                for i in range(self.steps+1):
                    if self.tmp_fs[i] != None:
                        self.tmp_fs[min(i+2,self.steps+1):] = [None] * (self.steps+1 - min(i+2,self.steps+1))
                        break
            
            if not size_max:
                self.write_out(self.tmp_fs[step_current], step_current)
                return True, self.in_f, self.out_f, size

            if size < size_max:
                if step_upper - step_lower > 1:
                    step_upper = step_current
                    step_current = int((step_lower + step_upper) / 2)
                    self.cb_msg.put(f'[<] Compressed {self.in_f_name} -> {self.out_f_name} but size {size} < limit {size_max}, recompressing')
                else:
                    self.write_out(self.tmp_fs[step_current], step_current)
                    return True, self.in_f, self.out_f, size
            else:
                if step_upper - step_lower > 1:
                    step_lower = step_current
                    step_current = round((step_lower + step_upper) / 2)
                    self.cb_msg.put(f'[>] Compressed {self.in_f_name} -> {self.out_f_name} but size {size} > limit {size_max}, recompressing')
                else:
                    if self.steps - step_current > 1:
                        self.write_out(self.tmp_fs[step_current + 1], step_current)
                        return True, self.in_f, self.out_f, size
                    else:
                        self.cb_msg.put(f'[F] Failed Compression {self.in_f_name} -> {self.out_f_name}, cannot get below limit {size_max} with lowest quality under current settings')
                        return False, self.in_f, self.out_f, size
    
    def write_out(self, data: bytes, step_current: Optional[int] = None):
        if os.path.splitext(self.out_f)[0] == 'none':
            self.out_f = None
        elif os.path.splitext(self.out_f)[0] == 'bytes':
            self.out_f = data
        else:
            with open(self.out_f, 'wb+') as f:
                f.write(data)

        if step_current:
            self.cb_msg.put(f'[S] Successful compression {self.in_f_name} -> {self.out_f_name} (step {step_current})')

    def frames_import(self):
        if self.in_f_ext in ('.tgs', '.lottie', '.json'):
            self.frames_import_lottie()
        else:
            self.frames_import_imageio()

    def frames_import_imageio(self):
        if self.in_f_ext in '.webp':
            # ffmpeg do not support webp decoding (yet)
            for frame in iio.imiter(self.in_f, plugin='pillow', mode='RGBA'):
                self.frames_raw.append(frame)
        else:
            frame_format = 'rgba'
            # Crashes when handling some webm in yuv420p and convert to rgba
            # https://github.com/PyAV-Org/PyAV/issues/1166
            metadata = iio.immeta(self.in_f, plugin='pyav', exclude_applied=False)
            context = None
            if metadata.get('video_format') == 'yuv420p':
                if metadata.get('alpha_mode') != '1':
                    frame_format = 'rgb24'
                if metadata.get('codec') == 'vp8':
                    context = CodecContext.create('v8', 'r')
                elif metadata.get('codec') == 'vp9':
                    context = CodecContext.create('libvpx-vp9', 'r')
            
            with av.open(self.in_f) as container:
                if not context:
                    context = container.streams.video[0].codec_context
                for packet in container.demux(video=0):
                    for frame in context.decode(packet):
                        frame = frame.to_ndarray(format=frame_format)
                        if frame_format == 'rgb24':
                            frame = np.dstack((frame, np.zeros(frame.shape[:2], dtype=np.uint8)+255))
                        self.frames_raw.append(frame)

    def frames_import_lottie(self):
        if self.in_f_ext == '.tgs':
            anim = LottieAnimation.from_tgs(self.in_f)
        else:
            if type(self.in_f) == str:
                anim = LottieAnimation.from_file(self.in_f)
            else:
                anim = LottieAnimation.from_data(self.in_f.read().decode('utf-8'))

        for i in range(anim.lottie_animation_get_totalframe()):
            frame = np.asarray(anim.render_pillow_frame(frame_num=i))
            self.frames_raw.append(frame)
        
        anim.lottie_animation_destroy()

    def frames_resize(self, frames_in: list[np.ndarray]) -> list[np.ndarray]:
        frames_out = []

        for frame in frames_in:
            im = Image.fromarray(frame, 'RGBA')
            width, height = im.size

            if self.res_w == None:
                self.res_w = width
            if self.res_h == None:
                self.res_h = height

            if width > height:
                width_new = self.res_w
                height_new = height * self.res_w // width
            else:
                height_new = self.res_h
                width_new = width * self.res_h // height
            im = im.resize((width_new, height_new), resample=Image.LANCZOS)
            im_new = Image.new('RGBA', (self.res_w, self.res_h), (0, 0, 0, 0))
            im_new.paste(im, ((self.res_w - width_new) // 2, (self.res_h - height_new) // 2))
            frames_out.append(np.asarray(im_new))
        
        return frames_out
    
    def frames_drop(self, frames_in: list[np.ndarray]) -> list[np.ndarray]:
        if not self.fps:
            return [frames_in[0]]

        frames_out = []
        
        frames_orig = CodecInfo.get_file_frames(self.in_f)
        fps_orig = CodecInfo.get_file_fps(self.in_f)
        duration_orig = frames_orig / fps_orig * 1000

        # fps_ratio: 1 frame in new anim equal to how many frame in old anim
        # speed_ratio: How much to speed up / slow down
        fps_ratio = fps_orig / self.fps
        if self.duration_min and self.duration_min > 0 and duration_orig < self.duration_min:
            speed_ratio = duration_orig / self.duration_min
        elif self.duration_max and self.duration_max > 0 and duration_orig > self.duration_max:
            speed_ratio = duration_orig / self.duration_max
        else:
            speed_ratio = 1

        frame_current = 0
        frame_current_float = 0
        while frame_current < len(frames_in):
            frames_out.append(frames_in[frame_current])
            frame_current_float += fps_ratio * speed_ratio
            frame_current = round(frame_current_float)

        return frames_out

    def frames_export(self):
        if self.out_f_ext in ('.apng', '.png') and self.fps:
            self.frames_export_apng()
        elif self.out_f_ext == '.png':
            self.frames_export_png()
        elif self.out_f_ext == '.webp' and self.fps:
            self.frames_export_webp()
        elif self.fps:
            self.frames_export_pyav()
        else:
            self.frames_export_pil()
    
    def frames_export_pil(self):
        image = Image.fromarray(self.frames_processed[0])
        image.save(
            self.tmp_f,
            format=self.out_f_ext.replace('.', ''),
            quality=self.quality
        )

    def frames_export_pyav(self):
        options = {}
        
        if type(self.quality) == int:
            options['quality'] = str(self.quality)
            options['lossless'] = '0'

        if self.out_f_ext == '.gif':
            codec = 'gif'
            pixel_format = 'rgb8'
            options['loop'] = '0'
        elif self.out_f_ext in ('.apng', '.png'):
            codec = 'apng'
            pixel_format = 'rgba'
            options['plays'] = '0'
        else:
            codec = 'vp9'
            pixel_format = 'yuva420p'
            options['loop'] = '0'
        
        with av.open(self.tmp_f, 'w', format=self.out_f_ext.replace('.', '')) as output:
            out_stream = output.add_stream(codec, rate=self.fps, options=options)
            out_stream.width = self.res_w
            out_stream.height = self.res_h
            out_stream.pix_fmt = pixel_format
            
            for frame in self.frames_processed:
                av_frame = av.VideoFrame.from_ndarray(frame, format='rgba')
                for packet in out_stream.encode(av_frame):
                    output.mux(packet)
            
            for packet in out_stream.encode():
                output.mux(packet)
    
    def frames_export_webp(self):
        config = webp.WebPConfig.new(quality=self.quality)
        enc = webp.WebPAnimEncoder.new(self.res_w, self.res_h)
        timestamp_ms = 0
        for frame in self.frames_processed:
            pic = webp.WebPPicture.from_numpy(frame)
            enc.encode_frame(pic, timestamp_ms, config=config)
            timestamp_ms += int(1 / self.fps * 1000)
        anim_data = enc.assemble(timestamp_ms)
        self.tmp_f.write(anim_data.buffer())

    def frames_export_png(self):
        image = Image.fromarray(self.frames_processed[0], 'RGBA')
        if self.color and self.color < 256:
            image_quant = image.quantize(colors=self.color, method=2)
        else:
            image_quant = image
        with io.BytesIO() as f:
            image_quant.save(f, format='png')
            f.seek(0)
            frame_optimized = oxipng.optimize_from_memory(f.read(), level=4)
            self.tmp_f.write(frame_optimized)

    def frames_export_apng(self):
        frames_concat = np.concatenate(self.frames_processed)
        image_concat = Image.fromarray(frames_concat, 'RGBA')
        if self.color and self.color < 256:
            image_quant = image_concat.quantize(colors=self.color, method=2)
        else:
            image_quant = image_concat

        for i in range(0, image_quant.height, self.res_h):
            with io.BytesIO() as f:
                image_quant.crop((0, i, image_quant.width, i+self.res_h)).save(f, format='png')
                f.seek(0)
                frame_optimized = oxipng.optimize_from_memory(f.read(), level=4)
            image_final = Image.open(io.BytesIO(frame_optimized)).convert('RGBA')
            frame_final = create_frame_from_rgba(np.array(image_final), image_final.width, image_final.height)
            frame_final.delay_num = int(1000 / self.fps)
            frame_final.delay_den = 1000
            self.apngasm.add_frame(frame_final)

        with CacheStore.get_cache_store(path=self.cache_dir) as tempdir:
            self.apngasm.assemble(os.path.join(tempdir, f'out{self.out_f_ext}'))

            with open(os.path.join(tempdir, f'out{self.out_f_ext}'), 'rb') as f:
                self.tmp_f.write(f.read())

        self.apngasm.reset()