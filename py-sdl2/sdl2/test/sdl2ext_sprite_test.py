import sys
import unittest
from ctypes import ArgumentError, POINTER, byref
from ..ext.resources import Resources
from .. import ext as sdl2ext
from ..surface import SDL_Surface, SDL_CreateRGBSurface, SDL_FreeSurface
from sdl2.video import SDL_Window, SDL_WINDOW_HIDDEN, SDL_DestroyWindow
from sdl2.render import SDL_Renderer, SDL_CreateWindowAndRenderer, \
    SDL_DestroyRenderer, SDL_CreateTexture, SDL_Texture, \
    SDL_TEXTUREACCESS_STATIC, SDL_TEXTUREACCESS_STREAMING, \
    SDL_TEXTUREACCESS_TARGET

_ISPYPY = hasattr(sys, "pypy_version_info")

RESOURCES = Resources(__file__, "resources")


class MSprite(sdl2ext.Sprite):
    def __init__(self, w=0, h=0):
        super(MSprite, self).__init__()
        self._size = w, h

    @property
    def size(self):
        return self._size


class SDL2ExtSpriteTest(unittest.TestCase):
    __tags__ = ["sdl", "sdl2ext"]

    def setUp(self):
        sdl2ext.init()

    def tearDown(self):
        sdl2ext.quit()

    def check_pixels(self, view, w, h, sprite, c1, c2, cx=0, cy=0):
        msg = "color mismatch at %d,%d: %d not in %s"
        cx = cx + sprite.x
        cy = cy + sprite.y
        cw, ch = sprite.size
        cmy = cy + ch
        cmx = cx + cw
        for y in range(w):
            for x in range(h):
                if cy <= y < cmy and cx <= x < cmx:
                    self.assertEqual(view[y][x], c1,
                                     msg % (x, y, view[y][x], c1))
                else:
                    self.assertTrue(view[y][x] in c2,
                                    msg % (x, y, view[y][x], c2))

    def test_SpriteFactory(self):
        factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
        self.assertIsInstance(factory, sdl2ext.SpriteFactory)
        self.assertEqual(factory.default_args, {})

        factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE, bananas="tasty")
        self.assertIsInstance(factory, sdl2ext.SpriteFactory)
        self.assertEqual(factory.default_args, {"bananas": "tasty"})

        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.RenderContext(window)

        factory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        self.assertIsInstance(factory, sdl2ext.SpriteFactory)

        factory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        self.assertIsInstance(factory, sdl2ext.SpriteFactory)
        self.assertEqual(factory.default_args, {"renderer": renderer})

        self.assertRaises(ValueError, sdl2ext.SpriteFactory, "Test")
        self.assertRaises(ValueError, sdl2ext.SpriteFactory, -456)
        self.assertRaises(ValueError, sdl2ext.SpriteFactory, 123)
        self.assertRaises(ValueError, sdl2ext.SpriteFactory, sdl2ext.TEXTURE)

    def test_SpriteFactory_create_sprite(self):
        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.RenderContext(window)
        tfactory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        sfactory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)

        for w in range(0, 100):
            for h in range(0, 100):
                for bpp in (1, 4, 8, 12, 15, 16, 24, 32):
                    sprite = sfactory.create_sprite(size=(w, h), bpp=bpp)
                    self.assertIsInstance(sprite, sdl2ext.SoftwareSprite)

                if w == 0 or h == 0:
                    self.assertRaises(sdl2ext.SDLError, tfactory.create_sprite,
                                      size=(w, h))
                    continue
                sprite = tfactory.create_sprite(size=(w, h))
                self.assertIsInstance(sprite, sdl2ext.TextureSprite)

    def test_SpriteFactory_create_software_sprite(self):
        factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
        for w in range(0, 100):
            for h in range(0, 100):
                for bpp in (1, 4, 8, 12, 15, 16, 24, 32):
                    sprite = factory.create_software_sprite((w, h), bpp)
                    self.assertIsInstance(sprite, sdl2ext.SoftwareSprite)

        #self.assertRaises(ValueError, factory.create_software_sprite, (-1,-1))
        #self.assertRaises(ValueError, factory.create_software_sprite, (-10,5))
        #self.assertRaises(ValueError, factory.create_software_sprite, (10,-5))
        self.assertRaises(TypeError, factory.create_software_sprite, size=None)
        self.assertRaises(sdl2ext.SDLError, factory.create_software_sprite,
                          size=(10, 10), bpp=-1)
        self.assertRaises(TypeError, factory.create_software_sprite, masks=5)
        self.assertRaises((ArgumentError, TypeError),
                          factory.create_software_sprite, size=(10, 10),
                          masks=(None, None, None, None))
        self.assertRaises((ArgumentError, TypeError),
                          factory.create_software_sprite, size=(10, 10),
                          masks=("Test", 1, 2, 3))

    def test_SpriteFactory_create_texture_sprite(self):
        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.RenderContext(window)
        factory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        for w in range(1, 100):
            for h in range(1, 100):
                sprite = factory.create_texture_sprite(renderer, size=(w, h))
                self.assertIsInstance(sprite, sdl2ext.TextureSprite)

        # Test different access flags
        for flag in (SDL_TEXTUREACCESS_STATIC, SDL_TEXTUREACCESS_STREAMING,
                     SDL_TEXTUREACCESS_TARGET, 22):
            sprite = factory.create_texture_sprite(renderer, size=(64, 64),
                                                   access=flag)
            self.assertIsInstance(sprite, sdl2ext.TextureSprite)

    def test_SpriteFactory_from_image(self):
        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.RenderContext(window)
        tfactory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        sfactory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)

        for suffix in ("tif", "png", "jpg"):
            imgname = RESOURCES.get_path("surfacetest.%s" % suffix)
            tsprite = tfactory.from_image(imgname)
            self.assertIsInstance(tsprite, sdl2ext.TextureSprite)
            ssprite = sfactory.from_image(imgname)
            self.assertIsInstance(ssprite, sdl2ext.SoftwareSprite)

        for factory in (tfactory, sfactory):
            self.assertRaises((AttributeError, TypeError, sdl2ext.SDLError),
                              factory.from_image, None)
            #self.assertRaises((IOError, SDLError),
            #                  factory.from_image, "banana")
            self.assertRaises((AttributeError, IOError, sdl2ext.SDLError),
                              factory.from_image, 12345)

    @unittest.skip("not implemented")
    def test_SpriteFactory_from_object(self):
        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.RenderContext(window)
        tfactory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        sfactory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)

    def test_SpriteFactory_from_surface(self):
        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.RenderContext(window)
        tfactory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        sfactory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)

        sf = SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0)
        tsprite = tfactory.from_surface(sf.contents)
        self.assertIsInstance(tsprite, sdl2ext.TextureSprite)
        ssprite = sfactory.from_surface(sf.contents)
        self.assertIsInstance(ssprite, sdl2ext.SoftwareSprite)
        SDL_FreeSurface(sf)

        for factory in (tfactory, sfactory):
            self.assertRaises((sdl2ext.SDLError, AttributeError, ArgumentError,
                               TypeError), factory.from_surface, None)
            self.assertRaises((AttributeError, ArgumentError, TypeError),
                              factory.from_surface, "test")
            # TODO: crashes pypy 2.0
            #self.assertRaises((AttributeError, ArgumentError, TypeError),
            #                  factory.from_surface, 1234)

    def test_SpriteFactory_from_text(self):
        sfactory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
        fm = sdl2ext.FontManager(RESOURCES.get_path("tuffy.ttf"))

        # No Fontmanager passed
        self.assertRaises(KeyError, sfactory.from_text, "Test")

        # Passing various keywords arguments
        sprite = sfactory.from_text("Test", fontmanager = fm)
        self.assertIsInstance(sprite, sdl2ext.SoftwareSprite)

        sprite = sfactory.from_text("Test", fontmanager = fm, alias="tuffy")
        self.assertIsInstance(sprite, sdl2ext.SoftwareSprite)

        # Get text from a texture sprite factory
        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.RenderContext(window)
        tfactory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE,
                                         renderer=renderer,
                                         fontmanager=fm)
        sprite = tfactory.from_text("Test", alias="tuffy")
        self.assertIsInstance(sprite, sdl2ext.TextureSprite)

    def test_SpriteRenderer(self):
        renderer = sdl2ext.SpriteRenderer()
        self.assertIsInstance(renderer, sdl2ext.SpriteRenderer)
        self.assertIsNotNone(renderer.sortfunc)
        self.assertTrue(sdl2ext.Sprite in renderer.componenttypes)

    def test_SpriteRenderer_sortfunc(self):
        def func(p):
            pass

        renderer = sdl2ext.SpriteRenderer()
        self.assertIsNotNone(renderer.sortfunc)
        renderer.sortfunc = func
        self.assertEqual(renderer.sortfunc, func)

        def setf(x, f):
            x.sortfunc = f
        self.assertRaises(TypeError, setf, renderer, None)
        self.assertRaises(TypeError, setf, renderer, "Test")
        self.assertRaises(TypeError, setf, renderer, 1234)

    @unittest.skip("not implemented")
    def test_SpriteRenderer_render(self):
        pass

    @unittest.skip("not implemented")
    def test_SpriteRenderer_process(self):
        pass

    def test_SoftwareSpriteRenderer(self):
        self.assertRaises(TypeError, sdl2ext.SoftwareSpriteRenderer)
        self.assertRaises(TypeError, sdl2ext.SoftwareSpriteRenderer, None)
        self.assertRaises(TypeError, sdl2ext.SoftwareSpriteRenderer, "Test")
        self.assertRaises(TypeError, sdl2ext.SoftwareSpriteRenderer, 12345)

        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.SoftwareSpriteRenderer(window)
        self.assertIsInstance(renderer, sdl2ext.SpriteRenderer)
        self.assertEqual(renderer.window, window.window)
        self.assertIsInstance(renderer.surface, SDL_Surface)

        renderer = sdl2ext.SoftwareSpriteRenderer(window.window)
        self.assertIsInstance(renderer, sdl2ext.SpriteRenderer)
        self.assertEqual(renderer.window, window.window)
        self.assertIsInstance(renderer.surface, SDL_Surface)

        self.assertIsNotNone(renderer.sortfunc)
        self.assertFalse(sdl2ext.Sprite in renderer.componenttypes)
        self.assertTrue(sdl2ext.SoftwareSprite in renderer.componenttypes)

    @unittest.skipIf(_ISPYPY, "PyPy's ctypes can't do byref(value, offset)")
    def test_SoftwareSpriteRenderer_render(self):
        sf1 = SDL_CreateRGBSurface(0, 12, 7, 32, 0, 0, 0, 0)
        sp1 = sdl2ext.SoftwareSprite(sf1.contents, True)
        sdl2ext.fill(sp1, 0xFF0000)

        sf2 = SDL_CreateRGBSurface(0, 3, 9, 32, 0, 0, 0, 0)
        sp2 = sdl2ext.SoftwareSprite(sf2.contents, True)
        sdl2ext.fill(sp2, 0x00FF00)
        sprites = [sp1, sp2]

        window = sdl2ext.Window("Test", size=(20, 20))
        renderer = sdl2ext.SoftwareSpriteRenderer(window)
        self.assertIsInstance(renderer, sdl2ext.SpriteRenderer)

        self.assertRaises(AttributeError, renderer.render, None, None, None)
        self.assertRaises(AttributeError, renderer.render, [None, None],
                          None, None)

        for x, y in ((0, 0), (3, 3), (20, 20), (1, 12), (5, 6)):
            sp1.position = x, y
            renderer.render(sp1)
            view = sdl2ext.PixelView(renderer.surface)
            self.check_pixels(view, 20, 20, sp1, 0xFF0000, (0x0,))
            del view
            sdl2ext.fill(renderer.surface, 0x0)
        sp1.position = 0, 0
        sp2.position = 14, 1
        renderer.render(sprites)
        view = sdl2ext.PixelView(renderer.surface)
        self.check_pixels(view, 20, 20, sp1, 0xFF0000, (0x0, 0x00FF00))
        self.check_pixels(view, 20, 20, sp2, 0x00FF00, (0x0, 0xFF0000))
        del view
        sdl2ext.fill(renderer.surface, 0x0)
        renderer.render(sprites, 1, 2)
        view = sdl2ext.PixelView(renderer.surface)
        self.check_pixels(view, 20, 20, sp1, 0xFF0000, (0x0, 0x00FF00), 1, 2)
        self.check_pixels(view, 20, 20, sp2, 0x00FF00, (0x0, 0xFF0000), 1, 2)
        del view

    @unittest.skipIf(_ISPYPY, "PyPy's ctypes can't do byref(value, offset)")
    def test_SoftwareSpriteRenderer_process(self):
        sf1 = SDL_CreateRGBSurface(0, 5, 10, 32, 0, 0, 0, 0)
        sp1 = sdl2ext.SoftwareSprite(sf1.contents, True)
        sp1.depth = 0
        sdl2ext.fill(sp1, 0xFF0000)

        sf2 = SDL_CreateRGBSurface(0, 5, 10, 32, 0, 0, 0, 0)
        sp2 = sdl2ext.SoftwareSprite(sf2.contents, True)
        sp2.depth = 99
        sdl2ext.fill(sp2, 0x00FF00)
        sprites = [sp1, sp2]

        window = sdl2ext.Window("Test", size=(20, 20))
        renderer = sdl2ext.SoftwareSpriteRenderer(window)

        renderer.process("fakeworld", sprites)
        view = sdl2ext.PixelView(renderer.surface)
        # Only sp2 wins, since its depth is higher
        self.check_pixels(view, 20, 20, sp1, 0x00FF00, (0x0,))
        self.check_pixels(view, 20, 20, sp2, 0x00FF00, (0x0,))
        del view

        self.assertRaises(TypeError, renderer.process, None, None)

    @unittest.skip("not implemented")
    def test_TextureSpriteRenderer(self):
        pass

    @unittest.skip("not implemented")
    def test_TextureSpriteRenderer_render(self):
        pass

    @unittest.skip("not implemented")
    def test_TextureSpriteRenderer_process(self):
        pass

    def test_Sprite(self):
        sprite = MSprite()
        self.assertIsInstance(sprite, MSprite)
        self.assertIsInstance(sprite, sdl2ext.Sprite)

    def test_Sprite_position_xy(self):
        sprite = MSprite()
        positions = [(x, y) for x in range(-50, 50) for y in range(-50, 50)]
        for x, y in positions:
            sprite.position = x, y
            self.assertEqual(sprite.position, (x, y))
            sprite.x = x + 1
            sprite.y = y + 1
            self.assertEqual(sprite.position, (x + 1, y + 1))

    def test_Sprite_area(self):
        for w in range(0, 200):
            for h in range(0, 200):
                sprite = MSprite(w, h)
                self.assertEqual(sprite.size, (w, h))
                self.assertEqual(sprite.area, (0, 0, w, h))
                sprite.position = w, h
                self.assertEqual(sprite.area, (w, h, 2 * w, 2 * h))

    def test_SoftwareSprite(self):
        self.assertRaises(TypeError, sdl2ext.SoftwareSprite, None, None)
        self.assertRaises(TypeError, sdl2ext.SoftwareSprite, None, True)
        self.assertRaises(TypeError, sdl2ext.SoftwareSprite, None, False)

        sf = SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0)
        sprite = sdl2ext.SoftwareSprite(sf.contents, False)
        # TODO: the following assert fails...
        # self.assertEqual(sprite.surface, sf.contents)
        self.assertFalse(sprite.free)

        sprite = sdl2ext.SoftwareSprite(sf.contents, True)
        # TODO: the following assert fails...
        # self.assertEqual(sprite.surface, sf.contents)
        self.assertTrue(sprite.free)

    def test_SoftwareSprite_repr(self):
        sf = SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0)
        sprite = sdl2ext.SoftwareSprite(sf.contents, True)
        self.assertEqual(repr(sprite), "SoftwareSprite(size=(10, 10), bpp=32)")

    def test_SoftwareSprite_position_xy(self):
        sf = SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0)
        sprite = sdl2ext.SoftwareSprite(sf.contents, True)
        self.assertIsInstance(sprite, sdl2ext.SoftwareSprite)
        self.assertEqual(sprite.position, (0, 0))
        positions = [(x, y) for x in range(-50, 50) for y in range(-50, 50)]
        for x, y in positions:
            sprite.position = x, y
            self.assertEqual(sprite.position, (x, y))
            sprite.x = x + 1
            sprite.y = y + 1
            self.assertEqual(sprite.position, (x + 1, y + 1))

    def test_SoftwareSprite_size(self):
        for w in range(0, 200):
            for h in range(0, 200):
                sf = SDL_CreateRGBSurface(0, w, h, 32, 0, 0, 0, 0)
                sprite = sdl2ext.SoftwareSprite(sf.contents, True)
                self.assertIsInstance(sprite, sdl2ext.SoftwareSprite)
                self.assertEqual(sprite.size, (w, h))

    def test_SoftwareSprite_area(self):
        sf = SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0)
        sprite = sdl2ext.SoftwareSprite(sf.contents, True)
        self.assertEqual(sprite.area, (0, 0, 10, 10))

        def setarea(s, v):
            s.area = v
        self.assertRaises(AttributeError, setarea, sprite, (1, 2, 3, 4))

        sprite.position = 7, 3
        self.assertEqual(sprite.area, (7, 3, 17, 13))
        sprite.position = -22, 99
        self.assertEqual(sprite.area, (-22, 99, -12, 109))

    def test_TextureSprite(self):
        window = POINTER(SDL_Window)()
        renderer = POINTER(SDL_Renderer)()
        SDL_CreateWindowAndRenderer(10, 10, SDL_WINDOW_HIDDEN,
                                    byref(window), byref(renderer))

        tex = SDL_CreateTexture(renderer, 0, 0, 10, 10)
        self.assertIsInstance(tex.contents, SDL_Texture)
        sprite = sdl2ext.TextureSprite(tex.contents)
        self.assertIsInstance(sprite, sdl2ext.TextureSprite)
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(window)

    def test_TextureSprite_position_xy(self):
        window = POINTER(SDL_Window)()
        renderer = POINTER(SDL_Renderer)()
        SDL_CreateWindowAndRenderer(10, 10, SDL_WINDOW_HIDDEN,
                                    byref(window), byref(renderer))
        tex = SDL_CreateTexture(renderer, 0, 0, 10, 10)
        self.assertIsInstance(tex.contents, SDL_Texture)
        sprite = sdl2ext.TextureSprite(tex.contents)
        self.assertIsInstance(sprite, sdl2ext.TextureSprite)
        self.assertEqual(sprite.position, (0, 0))
        positions = [(x, y) for x in range(-50, 50) for y in range(-50, 50)]
        for x, y in positions:
            sprite.position = x, y
            self.assertEqual(sprite.position, (x, y))
            sprite.x = x + 1
            sprite.y = y + 1
            self.assertEqual(sprite.position, (x + 1, y + 1))
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(window)

    def test_TextureSprite_size(self):
        window = POINTER(SDL_Window)()
        renderer = POINTER(SDL_Renderer)()
        SDL_CreateWindowAndRenderer(10, 10, SDL_WINDOW_HIDDEN,
                                    byref(window), byref(renderer))
        for w in range(1, 200):
            for h in range(1, 200):
                tex = SDL_CreateTexture(renderer, 0, 0, w, h)
                self.assertIsInstance(tex.contents, SDL_Texture)
                sprite = sdl2ext.TextureSprite(tex.contents)
                self.assertIsInstance(sprite, sdl2ext.TextureSprite)
                self.assertEqual(sprite.size, (w, h))
                del sprite
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(window)

    def test_TextureSprite_area(self):
        window = POINTER(SDL_Window)()
        renderer = POINTER(SDL_Renderer)()
        SDL_CreateWindowAndRenderer(10, 10, SDL_WINDOW_HIDDEN,
                                    byref(window), byref(renderer))
        tex = SDL_CreateTexture(renderer, 0, 0, 10, 20)
        self.assertIsInstance(tex.contents, SDL_Texture)
        sprite = sdl2ext.TextureSprite(tex.contents)
        self.assertIsInstance(sprite, sdl2ext.TextureSprite)
        self.assertEqual(sprite.area, (0, 0, 10, 20))

        def setarea(s, v):
            s.area = v

        self.assertRaises(AttributeError, setarea, sprite, (1, 2, 3, 4))
        sprite.position = 7, 3
        self.assertEqual(sprite.area, (7, 3, 17, 23))
        sprite.position = -22, 99
        self.assertEqual(sprite.area, (-22, 99, -12, 119))
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(window)

    @unittest.skip("not implemented")
    def test_RenderContext(self):
        pass

    @unittest.skip("not implemented")
    def test_RenderContext_color(self):
        pass

    @unittest.skip("not implemented")
    def test_RenderContext_blendmode(self):
        pass

    @unittest.skip("not implemented")
    def test_RenderContext_clear(self):
        pass

    @unittest.skipIf(_ISPYPY, "PyPy's ctypes can't do byref(value, offset)")
    def test_RenderContext_copy(self):
        surface = SDL_CreateRGBSurface(0, 128, 128, 32, 0, 0, 0, 0).contents
        sdl2ext.fill(surface, 0x0)
        renderer = sdl2ext.RenderContext(surface)
        factory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        w, h = 32, 32
        sp = factory.from_color(0xFF0000, (w, h))
        sp.x, sp.y = 40, 50
        renderer.copy(sp, (0, 0, w, h), (sp.x, sp.y, w, h))
        view = sdl2ext.PixelView(surface)
        self.check_pixels(view, 128, 128, sp, 0xFF0000, (0x0,))
        del view

    @unittest.skip("not implemented")
    def test_RenderContext_draw_line(self):
        pass

    @unittest.skip("not implemented")
    def test_RenderContext_draw_point(self):
        pass

    @unittest.skip("not implemented")
    def test_RenderContext_draw_rect(self):
        pass

    @unittest.skipIf(_ISPYPY, "PyPy's ctypes can't do byref(value, offset)")
    def test_RenderContext_fill(self):
        surface = SDL_CreateRGBSurface(0, 128, 128, 32, 0, 0, 0, 0).contents
        sdl2ext.fill(surface, 0x0)
        renderer = sdl2ext.RenderContext(surface)
        factory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        w, h = 32, 32
        sp = factory.from_color(0xFF0000, (w, h))
        sp.x, sp.y = 40, 50
        renderer.fill((sp.x, sp.y, w, h), 0x0000FF)
        view = sdl2ext.PixelView(surface)
        self.check_pixels(view, 128, 128, sp, 0x0000FF, (0x0,))
        del view


if __name__ == '__main__':
    sys.exit(unittest.main())
