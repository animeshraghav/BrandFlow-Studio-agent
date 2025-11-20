ToolClient = globals()['ToolClient']
make_id = globals()['make_id']
logger = globals()['logger']


class VisualAgent:
    """Visual Designer Agent: creates thumbnails, logo variants and social image assets.

    Uses ToolClient.generate_image (wraps an image API).
    """

    def __init__(self, tools: ToolClient):
        self.tools = tools

    def run_logo_variants(self, brand_profile: BrandProfile, n_variants: int = 3) -> List[Dict[str, Any]]:
        logger.info("[VisualAgent] generating %d logo variants for brand %s", n_variants, brand_profile.name)
        out = []
        for i in range(n_variants):
            prompt = f"Logo for {brand_profile.name} - {brand_profile.tagline} - style: {', '.join(brand_profile.tone)}"
            images = self.tools.generate_image(prompt, n=1)
            out.append({"variant_id": make_id("logo"), "prompt": prompt, "images": ["<img_placeholder>"]})
        return out

    def run_thumbnail(self, title: str, brand_profile: BrandProfile) -> Dict[str, Any]:
        prompt = f"Thumbnail for article '{title}' in brand style: {brand_profile.tone}. Use colors {brand_profile.palette}."
        imgs = self.tools.generate_image(prompt, n=1, size="1200x628")
        return {"id": make_id("thumb"), "prompt": prompt, "image": "<img_placeholder>"}