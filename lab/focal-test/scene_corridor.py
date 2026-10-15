# Scène test optique (15/10/2026) : un mannequin de 1,70 m devant une colonnade régulière (colonnes tous les 3 m sur 60 m).
# Rend un PNG par configuration capteur + focale. Pour 24/50/100 mm, la distance est proportionnelle à la focale
# (même taille de sujet, la perspective du fond change). Pour 35 mm plein format contre Super 35, même position de caméra.
# Usage : blender -b -P scene_couloir.py -- <dossier_sortie>
import bpy, math, sys, json, os

out = sys.argv[sys.argv.index("--") + 1]
os.makedirs(out, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def mat_obj(o, rgb):
    o.color = (*rgb, 1.0)

def add(kind, loc, scale=(1, 1, 1), rgb=(0.7, 0.7, 0.7), **kw):
    getattr(bpy.ops.mesh, kind)(location=loc, **kw)
    o = bpy.context.active_object
    o.scale = scale
    mat_obj(o, rgb)
    return o

# sol et murs
add("primitive_plane_add", (0, 30, 0), (6, 45, 1), (0.55, 0.52, 0.48))
add("primitive_cube_add", (-6.5, 30, 3), (0.2, 45, 3), (0.80, 0.78, 0.74))
add("primitive_cube_add", (6.5, 30, 3), (0.2, 45, 3), (0.80, 0.78, 0.74))
add("primitive_cube_add", (0, 64, 3), (6.5, 0.2, 3), (0.62, 0.66, 0.70))
add("primitive_cube_add", (0, 63.7, 1.1), (0.6, 0.1, 1.1), (0.25, 0.22, 0.20))  # porte
# colonnade : colonnes tous les 3 m, des deux côtés
for i in range(21):
    y = 3 * i
    for x in (-3.2, 3.2):
        add("primitive_cylinder_add", (x, y, 2.0), (0.28, 0.28, 2.0), (0.88, 0.86, 0.82), vertices=24)
# lampes au sol tous les 6 m (repères de distance)
for i in range(11):
    add("primitive_cube_add", (0, 6 * i + 1.5, 0.05), (0.15, 0.15, 0.05), (0.9, 0.75, 0.2))
# mannequin 1,70 m à l'origine
add("primitive_cylinder_add", (-0.11, 0, 0.42), (0.08, 0.08, 0.42), (0.20, 0.22, 0.30), vertices=16)
add("primitive_cylinder_add", (0.11, 0, 0.42), (0.08, 0.08, 0.42), (0.20, 0.22, 0.30), vertices=16)
add("primitive_cylinder_add", (0, 0, 1.15), (0.21, 0.13, 0.32), (0.65, 0.15, 0.12), vertices=24)
add("primitive_cylinder_add", (-0.29, 0, 1.12), (0.055, 0.055, 0.3), (0.65, 0.15, 0.12), vertices=12)
add("primitive_cylinder_add", (0.29, 0, 1.12), (0.055, 0.055, 0.3), (0.65, 0.15, 0.12), vertices=12)
add("primitive_uv_sphere_add", (0, 0, 1.58), (0.11, 0.12, 0.13), (0.85, 0.70, 0.60))

# lumière (Workbench : éclairage studio, ombres)
sc.render.engine = "BLENDER_WORKBENCH"
sc.display.shading.light = "STUDIO"
sc.display.shading.color_type = "OBJECT"
sc.display.shading.show_shadows = True
sc.display.shading.show_cavity = True
sc.render.resolution_x, sc.render.resolution_y = 1344, 768
sc.render.image_settings.file_format = "PNG"

cam_data = bpy.data.cameras.new("cam")
cam = bpy.data.objects.new("cam", cam_data)
sc.collection.objects.link(cam)
sc.camera = cam
cam_data.sensor_fit = "HORIZONTAL"

K = 0.14  # m par mm de focale en plein format : le sujet occupe ~60 % de la hauteur d'image
configs = [
    ("f24_plein-format", 24, 36.0, 24 * K),
    ("f50_plein-format", 50, 36.0, 50 * K),
    ("f100_plein-format", 100, 36.0, 100 * K),
    ("f35_plein-format", 35, 36.0, 35 * K),
    ("f35_super35", 35, 24.89, 35 * K),
]
meta = []
for name, f, sw, d in configs:
    cam_data.lens = f
    cam_data.sensor_width = sw
    cam.location = (0, -d, 1.45)
    tilt = math.atan2(1.45 - 1.0, d)  # vise le bassin du mannequin
    cam.rotation_euler = (math.radians(90) - tilt, 0, 0)
    sc.render.filepath = os.path.join(out, name + ".png")
    bpy.ops.render.render(write_still=True)
    hfov = math.degrees(2 * math.atan(sw / (2 * f)))
    meta.append({"nom": name, "focale_mm": f, "capteur_mm": sw, "distance_m": round(d, 2), "angle_horizontal_deg": round(hfov, 2)})
json.dump(meta, open(os.path.join(out, "cameras.json"), "w"), indent=1)
print("RENDUS OK", len(meta))
