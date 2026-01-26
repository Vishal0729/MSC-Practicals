import pandas as pd
Base = "D:/MSC Practicals/Data Science/Practical - 3/Outputs/"
def save_units(unit_type, file, ranges, thickness=False):
    """Generate and save shipping units (Container/Box/Product)"""
    df = pd.DataFrame([
        {
            "ShipType": unit_type,
            "UnitNumber": f"{unit_type[0]}{i+1:06d}",
            "Length": l/10 if unit_type!="Container" else l,
            "Width": w/10 if unit_type!="Container" else w,
            "Height": h/10 if unit_type!="Container" else h,
            **({"Thickness": t/5, "BoxVolume": l*w*h/1000, "ProductVolume": ((l-t)*(w-t)*(h-t))/1000} if thickness else
               {"ContainerVolume": l*w*h} if unit_type=="Container" else {"ProductVolume": l*w*h/1000})
        }
        for i,l in enumerate(range(*ranges["L"]))
        for w in range(*ranges["W"])
        for h in range(*ranges["H"])
        for t in (ranges["T"] if thickness else [0])
        if not thickness or (l-t)*(w-t)*(h-t) > 0
    ])
    df.to_csv(file, index=False)
    return df
# Generate all units
save_units("Container", f"{Base}/Retrieve_Container.csv", {"L":(1,21),"W":(1,10),"H":(1,6)})
save_units("Box", f"{Base}/Retrieve_Box.csv", {"L":(1,21),"W":(1,21),"H":(1,21),"T":(0,6)}, thickness=True)
save_units("Product", f"{Base}/Retrieve_Product.csv", {"L":(1,21),"W":(1,21),"H":(1,21)})

print("Containers, Boxes, Products generated successfully!")
