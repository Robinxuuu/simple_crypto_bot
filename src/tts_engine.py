import platform, subprocess

def speak(text: str):
    # macOS 原生
    if platform.system() == "Darwin":
        subprocess.run(["say","-v","Meijia", text])
        return
    # 其他平台：pyttsx3
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', 185)
        engine.say(text)
        engine.runAndWait()
    except Exception:
        print("[TTS Fallback] 无法合成语音，改为打印：\n", text)

# 以下为测试代码
'''
if __name__ == "__main__":
    test_text = "这里是测试语音。今天是2023年10月15日，比特币价格突破三万美元。"

    print("开始测试文本转语音功能...")
    print(f"测试文本: {test_text}")

    # 调用speak函数
    speak(test_text)

    print("语音播放完成（如果没有听到声音，请检查系统音频设置）")
'''