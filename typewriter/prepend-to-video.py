"""

export typewriter as a movie in frames by running python script

creating a video from the frames

    ffmpeg -framerate 25 -i typing-frames/%06d.png -s 640x480 -c:v libx264 -pix_fmt yuv420p -r 30 silent-video.mkv

we can also generate audio - but it sucks:
    
    ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 silent-video.mkv
    ffmpeg -stream_loop -1 -i single-click.mp3 -t 8.66 -c:a aac looped-audio.m4a
    ffmpeg -i silent-video.mkv -i looped-audio.m4a -c:v copy -c:a aac -shortest final-output.mkv


screen grab - requires perfect positioning - still no  audio
    ffmpeg -f gdigrab -framerate 25 -offset_x X -offset_y Y -video_size 640x480 -i desktop -c:v libx264 -pix_fmt yuv420p -r 25 output.mkv

    
=>  conclusion: 
        just use OBS to capture as video
        use capture window
        add a crop filter to remove title bar etc

#  from 1920x1080
# -filter:v "crop=800:600:560:240"
#            crop=width:height:x:y
ffmpeg -i input1.mkv -c:v libx264  -filter:v "crop=800:600:560:240" -level 6.2 -crf 18  -preset slow -g  5  -bf 1  -b_strategy 0   input2.mkv

# clip
ffmpeg -i input2.mkv -c:v libx264 -level 6.2 -crf 18   -ss 00:00.300     -to 00:00:12.000         input3.mkv

# rescale
ffmpeg -i input3.mkv -c:v libx264  -s 1920x1080 -level 6.2 -crf 18   input4.mkv


pip install playwright
playwright install chromium

"""
from   pathlib import Path
import time
from playwright.sync_api import sync_playwright

def main():

    """
        launching a headless browser and capturing frames

        html page needs to resize body to 0, 0, 640, 480

        html page needs to set window.animationDone = true
    """

    htmlPath = Path("typing-4.html").resolve()   # your HTML file
    outDir = Path("typing-frames")
    outDir.mkdir(exist_ok=True)

    width  = 640
    height = 480
    fps    =  25

    frameDuration = 1.0 / fps
    frameIndex = 0

    print(f"init done")

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True, args=[f"--window-size={width},{height}"])
        context = browser.new_context(viewport={"width": width, "height": height})
        page = context.new_page()

        print(f"browser should be open")

        page.goto(htmlPath.as_uri())
        # start the animation (simulate your click-anywhere)
        page.click("body")

        lastFrameTime = time.perf_counter()

        # loop until the HTML tells us it finished
        while True:
            now = time.perf_counter()
            elapsed = now - lastFrameTime
            if elapsed < frameDuration:
                time.sleep(frameDuration - elapsed)
            lastFrameTime = time.perf_counter()

            framePath = outDir / f"{frameIndex:06d}.png"
            page.screenshot(path=str(framePath), clip={"x": 0, "y": 0, "width": width, "height": height})
            frameIndex += 1

            isDone = page.evaluate("window.animationDone === true")
            if isDone:
                # grab one last frame to be safe
                framePath = outDir / f"{frameIndex:06d}.png"
                page.screenshot(path=str(framePath), clip={"x": 0, "y": 0, "width": width, "height": height})
                break

        browser.close()

if __name__ == "__main__":
    main()

