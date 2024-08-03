import ffmpeg


class VideoDownloader:
    def __init__(self, video_file: str):
        self.video_file = video_file
        self.in_file = ffmpeg.input(self.video_file).audio

    def extract(self, start_time: str, end_time: str, output_file: str) -> str:
        try:
            final_output_file = output_file + '.mp3'
            (
                self.in_file
                .filter('atrim', start=start_time, end=end_time)
                .filter('asetpts', 'PTS-STARTPTS')
                .output(final_output_file, format='mp3', acodec='libmp3lame')
                .run(overwrite_output=True)
            )
            print(f"Extracted video segment saved as {final_output_file}")
            return final_output_file
        except ffmpeg.Error as e:
            print(f"Error occurred: {e.stderr}")
            return None
