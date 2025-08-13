import os
import openai
from PIL import Image
from moviepy.editor import *
from .base_agent import BaseAgent
from app import db
from app.models import ContentProject

class ContentCreatorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="content_creator_v2",
            capabilities=["image_generation", "video_editing", "copywriting"]
        )
        self.openai_key = os.getenv('OPENAI_API_KEY')
        self.stable_diffusion_url = os.getenv('STABLE_DIFFUSION_URL')
        
    def generate_image(self, prompt, project_id):
        """Generate HD image using Stable Diffusion"""
        try:
            # Call Stable Diffusion API
            response = self._call_api(
                url=self.stable_diffusion_url,
                payload={
                    "prompt": prompt,
                    "negative_prompt": "blurry, low quality",
                    "width": 1024,
                    "height": 1024
                }
            )
            
            # Save to project directory
            project = ContentProject.query.get(project_id)
            filename = f"generated_{project_id}_{uuid.uuid4()}.png"
            filepath = os.path.join(project.directory, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            # Update project record
            project.assets.append(filename)
            db.session.commit()
            
            return {"status": "success", "filepath": filepath}
            
        except Exception as e:
            self.log_error(f"Image generation failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    def create_video_reel(self, images, audio_path, project_id):
        """Combine images and audio into video reel"""
        try:
            # Create clips from images
            clips = [ImageClip(img).set_duration(3) for img in images]
            
            # Combine with audio
            video = concatenate_videoclips(clips)
            video = video.set_audio(AudioFileClip(audio_path))
            
            # Save output
            project = ContentProject.query.get(project_id)
            output_path = os.path.join(project.directory, f"reel_{project_id}.mp4")
            video.write_videofile(output_path, fps=24)
            
            return {"status": "success", "output_path": output_path}
            
        except Exception as e:
            self.log_error(f"Video creation failed: {str(e)}")
            return {"status": "error", "message": str(e)}
