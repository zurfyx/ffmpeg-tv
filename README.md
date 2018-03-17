# FFmpeg TV

> TV video encoding without hassle.

A solution to [How can I get high quality/low size MP4s like the LOL release group?](https://superuser.com/questions/582198/how-can-i-get-high-quality-low-size-mp4s-like-the-lol-release-group)

## What are TV standards or scene guides?

A set of guidelines that serve as a standard to distribute videos.

See [scenerules latest TV standards](https://scenerules.org/t.html?id=tvx2642k16.nfo).

## Getting started

Requirements:

- ffmpeg

```
python3 ffmpeg-tv.py input.mp4 output.mkv
```

See [ffmpeg-tv.py](ffmpeg-tv.py) for the complete set of configurations (such as `--scale "1920:1080"`).

## Special thanks

- [scenerules](https://scenerules.org)
- [slhck](https://superuser.com/users/48078/slhck)

## License

MIT © [Gerard Rovira Sánchez](//zurfyx.com)