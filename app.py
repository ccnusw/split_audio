import streamlit as st
from moviepy.editor import *
import os
import tempfile

# -----------------------------------------------------------------------------
# 1. UI/UX 设计与页面配置 (Page Config & UI Design)
# -----------------------------------------------------------------------------
# 使用 st.set_page_config() 来设置页面标题、图标和布局
st.set_page_config(
    page_title="视频音轨分离器 | Video to Audio Extractor",
    page_icon="🎵",
    layout="centered", # 'centered' 或 'wide'
    initial_sidebar_state="auto"
)

# --- 应用标题和描述 ---
st.title("🎬 视频音轨分离器 ✨")
st.markdown("轻松几步，从您的视频文件中提取纯净的音频。上传视频，选择格式，即刻下载！")

# -----------------------------------------------------------------------------
# 2. 核心功能实现 (Core Functionality)
# -----------------------------------------------------------------------------

# --- 步骤 1: 文件上传 ---
st.header("第一步：上传您的视频文件")
uploaded_file = st.file_uploader(
    "请选择或拖拽一个视频文件",
    type=['mp4', 'mov', 'avi', 'mkv', 'wmv'], # 支持的视频格式
    help="支持常见的视频格式，如MP4, MOV, AVI等。"
)

# 如果用户上传了文件，则显示后续操作
if uploaded_file is not None:
    # 显示上传的文件信息
    st.video(uploaded_file)
    file_details = {"文件名": uploaded_file.name, "文件类型": uploaded_file.type, "文件大小 (MB)": f"{uploaded_file.size / (1024 * 1024):.2f}"}
    st.write("上传文件详情：")
    st.json(file_details)
    
    st.divider() # 添加分割线，使界面更清晰

    # --- 步骤 2: 配置输出选项 ---
    st.header("第二步：选择您想要的音频格式")
    
    col1, col2 = st.columns([2, 3]) # 创建两列来布局选项
    
    with col1:
        output_format = st.selectbox(
            "输出格式",
            ("mp3", "wav", "aac", "ogg"),
            index=0, # 默认选中第一个 'mp3'
            help="MP3格式通用且文件小，WAV格式为无损但文件较大。"
        )

    # 如果选择mp3，提供比特率选项
    bitrate = None
    if output_format == "mp3":
        with col2:
            bitrate = st.select_slider(
                "MP3 音质 (比特率)",
                options=['96k', '128k', '192k', '256k', '320k'],
                value='192k', # 默认值
                help="比特率越高，音质越好，文件也越大。192kbps为标准音质。"
            )

    st.divider()

    # --- 步骤 3: 处理与下载 ---
    st.header("第三步：开始转换并下载")
    
    if st.button("🚀 开始提取音频", type="primary", use_container_width=True):
        
        video_clip = None
        output_audio_path = None
        video_path = None
        
        # 使用临时文件来处理上传，这是一种良好的实践
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as temp_video_file:
            temp_video_file.write(uploaded_file.getvalue())
            video_path = temp_video_file.name

        try:
            with st.spinner(f"正在处理视频... 请耐心等待 ⏳"):
                # 使用 MoviePy 加载视频
                video_clip = VideoFileClip(video_path)

                # 【修复】检查视频音轨
                if video_clip.audio is None:
                    # 如果视频没有音轨，显示错误
                    st.error("处理失败：您上传的视频文件不包含任何音轨。")
                else:
                    # 如果有音轨，则继续执行提取和显示逻辑
                    output_audio_path = os.path.splitext(video_path)[0] + f".{output_format}"

                    # 提取音频并写入文件
                    # logger=None 可以避免在streamlit控制台打印过多的moviepy日志
                    if output_format == "mp3":
                        video_clip.audio.write_audiofile(output_audio_path, bitrate=bitrate, logger=None)
                    else:
                        video_clip.audio.write_audiofile(output_audio_path, logger=None)
                    
                    st.success("🎉 音频提取成功！")
                    
                    # --- 结果展示 ---
                    st.subheader("🎵 在线试听")
                    
                    with open(output_audio_path, 'rb') as audio_file:
                        audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format=f'audio/{output_format}')

                    # --- 提供下载按钮 ---
                    st.subheader("💾 下载您的音频文件")
                    # 再次读取文件以供下载
                    with open(output_audio_path, 'rb') as audio_file_to_download:
                        st.download_button(
                            label=f"点击下载 {os.path.basename(output_audio_path)}",
                            data=audio_file_to_download,
                            file_name=f"extracted_audio.{output_format}",
                            mime=f"audio/{output_format}",
                            use_container_width=True
                        )

        except Exception as e:
            st.error(f"处理过程中发生错误：{e}")
            st.error("请尝试更换视频文件或检查文件是否完好。")
        
        # 使用 finally 确保资源总是被释放
        finally:
            # 无论处理成功与否，此代码块都将被执行
            # 确保关闭所有已打开的媒体文件
            if video_clip:
                video_clip.close()
            
            # 安全地删除临时文件
            if output_audio_path and os.path.exists(output_audio_path):
                os.remove(output_audio_path)
            if video_path and os.path.exists(video_path):
                os.remove(video_path)

# --- 页脚 ---
st.markdown("---")
st.markdown("本软件由沈威开发 | 使用中有任何问题可以发邮件至sw@ccnu.edu.cn")