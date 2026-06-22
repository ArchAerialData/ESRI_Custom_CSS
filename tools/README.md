# Asset Tools

Optional repo-local tools for preparing client logo assets. These tools are not part of the CSS delivery path.

## Vector Trace A Logo

Install dependencies once:

```powershell
npm.cmd install
```

Trace an image to SVG:

```powershell
npm.cmd run trace-logo -- --input clients/faulconer_energy/logos/cover/faulconer_mark.png --svg clients/faulconer_energy/logos/cover/faulconer_mark.svg --trim --colors 4
```

Trace and also render a PNG preview:

```powershell
npm.cmd run trace-logo -- --input clients/faulconer_energy/logos/cover/faulconer_mark.png --svg clients/faulconer_energy/logos/cover/faulconer_mark.svg --png clients/faulconer_energy/logos/cover/faulconer_mark_trace.png --png-size 400 --trim --colors 4
```

For logos on a white JPG background, remove near-white pixels before tracing:

```powershell
npm.cmd run trace-logo -- --input clients/faulconer_energy/logos/cover/faulconer.jpg --svg clients/faulconer_energy/logos/cover/faulconer.svg --remove-white --trim --colors 6
```

For brand logos with small accent colors, prefer a fixed palette so the tracer does not quantize away the small color region:

```powershell
npm.cmd run trace-logo -- --input clients/faulconer_energy/logos/cover/faulconer_mark.png --svg clients/faulconer_energy/logos/cover/faulconer_mark.svg --png clients/faulconer_energy/logos/cover/faulconer_mark_trace.png --png-size 400 --trim --palette "#024ab8,#eb2518,#ffffff"
```

Useful options:

- `--remove-white`: treats near-white pixels as transparent before tracing.
- `--white-threshold 245`: changes the near-white cutoff.
- `--palette "#024ab8,#eb2518,#ffffff"`: forces a fixed color palette.
- `--ltres`, `--qtres`, `--pathomit`, `--blur`: tune ImageTracer path detail and cleanup.

On shells where npm argument forwarding works normally, `npm run trace-logo -- ...` is equivalent. On Windows PowerShell, `npm.cmd run ...` avoids the `npm.ps1` shim swallowing forwarded arguments.
