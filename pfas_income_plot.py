"""Test file."""
import math
import matplotlib
import matplotlib.pyplot as plt
import geopandas

# Source file: https://gis-michigan.opendata.arcgis.com/datasets/egle::miejscreen-draft-data/about
CENSUS_DATA_SHAPEFILE = "MiEJScreen_Draft_Data/MiEJScreen_Draft_Data.shp"
# Source file: https://gis-egle.hub.arcgis.com/datasets/egle::michigan-pfas-sites/about
# PFAS_SITES_DATA = "Michigan_PFAS_Sites/Michigan_PFAS_Sites.shp"
# Source file: https://gis-egle.hub.arcgis.com/datasets/egle::pfas-surface-water-sampling/about
WATER_SAMPLING_SHAPEFILE = "PFAS_Surface_Water_Sampling/PFAS_Surface_Water_Sampling.shp"

def main():
    """The main function."""
    census_data = geopandas.read_file(CENSUS_DATA_SHAPEFILE).to_crs("EPSG:4326")
    # pfas_sites_data = geopandas.read_file(PFAS_SITES_DATA).to_crs("EPSG:4326")
    water_data = geopandas.read_file(WATER_SAMPLING_SHAPEFILE).to_crs("EPSG:4326")

    # for col in water_data:
    #     if col in "CAS1763231_PFOS":
    #         print(len(col))
    #     if col in "CAS335671_PFOA":
    #         print(len(col))


    legend_label = "Proximity to Hazardous Waste Facilities (percentage)"
    tite_label = "Proximity to Hazardous Waste Facilities"
    file_name = "Proximity-to-Hazardous-Waste-Facilities"
    census_data_col = "ProximityHazWasteFacilities"[:10]
    census_data[census_data_col] = [datum if datum > 0 else None
                                 for datum in census_data[census_data_col]]

    pfas = [("PFOA","CAS335671_PFOA"[:10]), ("PFOS","CAS1763231_PFOS"[:10])]
    for pfa in pfas:
        water_data[pfa[1]] = [
            math.log10(float(datum)) if datum and float(datum) > 4.0 else None
            for datum in water_data[pfa[1]]]

        _,ax = plt.subplots(figsize=(10,10))

        cm = matplotlib.colormaps.get_cmap('YlOrRd')
        census_data.plot(ax=ax, column=census_data_col, legend=True,
                        cmap=cm,
                        legend_kwds={
                            "label": legend_label,
                            "shrink": .25,
                            "location": "left",
                        },
                        missing_kwds={
                            "color": "lightgrey",
                            "edgecolor": "red",
                            "hatch": "///",
                            "label": "Missing values",
                        },
        )
        cm = matplotlib.colormaps.get_cmap('cool')
        water_data.plot(ax=ax, column=pfa[1], marker=".",
                        c=water_data[pfa[1]],
                        cmap=cm,
                        legend=True,
                        legend_kwds={
                            "label": f"{pfa[0]} Concentration in log10(PPT)\nand PPT>4.0",
                            "shrink": .25,
                        },
                        markersize=9,
                    )
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title(f"{pfa[0]} Sites Displayed on {tite_label} in Michigan")
        plt.savefig(f"output/{pfa[0]}/{pfa[0]}-vs-{file_name}.jpg", dpi=2000, bbox_inches='tight')
        plt.clf()


if __name__ == "__main__":
    main()
