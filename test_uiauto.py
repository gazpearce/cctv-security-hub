import uiautomation as auto

root = auto.GetRootControl()
children = root.GetChildren()
print("Total top-level windows:", len(children))
for w in children:
    name = w.Name
    cls = w.ClassName
    if "Chrome" in cls or "chrome" in name.lower() or "google" in name.lower():
        print(f"Found Chrome Window: Name='{name}', Class='{cls}', BoundingBox={w.BoundingRectangle}")
