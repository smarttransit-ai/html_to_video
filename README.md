```python
import html_to_video.html_to_video as htov

with open('./override-fade.js', 'r') as f:
    script = f.read()

htov.create_video_from_htmls(
    plot_files, 
    './results/videos/video.avi', 
    script_to_append=script,
    append_inplace=True,
    fps=5,
    post_render_wait=0.3
)