const API_URL = "https://blueprint-ai-38p.onrender.com/api/generate-blueprint";

const generateButton =
    document.getElementById("generateButton");

const clearButton =
    document.getElementById("clearButton");

const downloadButton =
    document.getElementById("downloadButton");

const message =
    document.getElementById("message");

const svg =
    document.getElementById("blueprint");

const emptyState =
    document.getElementById("emptyState");

const statistics =
    document.getElementById("statistics");

const legend =
    document.getElementById("legend");

generateButton.addEventListener(
    "click",
    generateBlueprint
);

clearButton.addEventListener(
    "click",
    clearBlueprint
);

downloadButton.addEventListener(
    "click",
    downloadBlueprint
);


async function generateBlueprint() {
    const requirements = collectRequirements();

    if (!validateRequirements(requirements)) {
        return;
    }

    generateButton.disabled = true;
    generateButton.textContent = "Generating...";
    message.textContent = "Creating your blueprint...";
    message.style.color = "#2563eb";

    try {
        const response = await fetch(
            API_URL,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(requirements)
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.message ||
                "Blueprint generation failed."
            );
        }

        drawBlueprint(result.blueprint);
        updateStatistics(result.blueprint);
        createLegend(result.blueprint.rooms);

        emptyState.style.display = "none";
        svg.style.display = "block";
        statistics.classList.remove("hidden");
        legend.classList.remove("hidden");

        downloadButton.disabled = false;

        message.textContent =
            "Blueprint generated successfully.";

        message.style.color = "#15803d";

    } catch (error) {
        console.error(error);

        message.textContent =
            error.message ||
            "Unable to connect to the backend.";

        message.style.color = "#dc2626";

    } finally {
        generateButton.disabled = false;
        generateButton.textContent =
            "Generate Blueprint";
    }
}


function collectRequirements() {
    return {
        project_name:
            document.getElementById(
                "projectName"
            ).value.trim(),

        project_type:
            document.getElementById(
                "projectType"
            ).value,

        floors:
            Number(
                document.getElementById(
                    "floors"
                ).value
            ),

        plot_width:
            Number(
                document.getElementById(
                    "plotWidth"
                ).value
            ),

        plot_length:
            Number(
                document.getElementById(
                    "plotLength"
                ).value
            ),

        bedrooms:
            Number(
                document.getElementById(
                    "bedrooms"
                ).value
            ),

        bathrooms:
            Number(
                document.getElementById(
                    "bathrooms"
                ).value
            ),

        include_living_room:
            document.getElementById(
                "includeLivingRoom"
            ).checked,

        include_kitchen:
            document.getElementById(
                "includeKitchen"
            ).checked,

        include_parking:
            document.getElementById(
                "includeParking"
            ).checked,

        include_balcony:
            document.getElementById(
                "includeBalcony"
            ).checked,

        include_dining_room:
            document.getElementById(
                "includeDiningRoom"
            ).checked,

        include_study_room:
            document.getElementById(
                "includeStudyRoom"
            ).checked
    };
}


function validateRequirements(data) {
    if (!data.project_name) {
        showError("Please enter a project name.");
        return false;
    }

    if (
        data.plot_width < 10 ||
        data.plot_length < 10
    ) {
        showError(
            "Plot width and length must be at least 10 feet."
        );

        return false;
    }

    if (
        data.bedrooms < 1 ||
        data.bathrooms < 1
    ) {
        showError(
            "Enter valid bedroom and bathroom values."
        );

        return false;
    }

    return true;
}


function showError(errorMessage) {
    message.textContent = errorMessage;
    message.style.color = "#dc2626";
}


function drawBlueprint(blueprint) {
    svg.innerHTML = "";

    const namespace =
        "http://www.w3.org/2000/svg";

    const startX = 80;
    const startY = 100;
    const drawingWidth = 740;
    const drawingHeight = 460;

    const scaleX =
        drawingWidth / blueprint.plot.width;

    const scaleY =
        drawingHeight / blueprint.plot.length;

    addBlueprintTitle(
        namespace,
        blueprint
    );

    addPlotBorder(
        namespace,
        startX,
        startY,
        drawingWidth,
        drawingHeight
    );

    blueprint.rooms.forEach(
        (room, index) => {
            const x =
                startX + room.x * scaleX;

            const y =
                startY + room.y * scaleY;

            const width =
                room.width * scaleX;

            const height =
                room.length * scaleY;

            drawRoom(
                namespace,
                room,
                index,
                x,
                y,
                width,
                height
            );
        }
    );

    addPlotDimensions(
        namespace,
        blueprint,
        startX,
        startY,
        drawingWidth,
        drawingHeight
    );

    addNorthArrow(namespace);
}


function addBlueprintTitle(
    namespace,
    blueprint
) {
    const title =
        document.createElementNS(
            namespace,
            "text"
        );

    title.setAttribute("x", "450");
    title.setAttribute("y", "38");
    title.setAttribute(
        "text-anchor",
        "middle"
    );

    title.setAttribute(
        "font-size",
        "25"
    );

    title.setAttribute(
        "font-weight",
        "700"
    );

    title.setAttribute(
        "fill",
        "#0f172a"
    );

    title.textContent =
        blueprint.project_name;

    svg.appendChild(title);

    const subtitle =
        document.createElementNS(
            namespace,
            "text"
        );

    subtitle.setAttribute("x", "450");
    subtitle.setAttribute("y", "65");
    subtitle.setAttribute(
        "text-anchor",
        "middle"
    );

    subtitle.setAttribute(
        "font-size",
        "14"
    );

    subtitle.setAttribute(
        "fill",
        "#64748b"
    );

    subtitle.textContent =
        `${blueprint.project_type} Conceptual Floor Plan`;

    svg.appendChild(subtitle);
}


function addPlotBorder(
    namespace,
    x,
    y,
    width,
    height
) {
    const border =
        document.createElementNS(
            namespace,
            "rect"
        );

    border.setAttribute("x", x);
    border.setAttribute("y", y);
    border.setAttribute("width", width);
    border.setAttribute("height", height);
    border.setAttribute("fill", "#ffffff");
    border.setAttribute("stroke", "#0f172a");
    border.setAttribute("stroke-width", "7");

    svg.appendChild(border);
}


function drawRoom(
    namespace,
    room,
    index,
    x,
    y,
    width,
    height
) {
    const color =
        getRoomColor(room.name);

    const rectangle =
        document.createElementNS(
            namespace,
            "rect"
        );

    rectangle.setAttribute("x", x);
    rectangle.setAttribute("y", y);
    rectangle.setAttribute("width", width);
    rectangle.setAttribute("height", height);
    rectangle.setAttribute("fill", color);
    rectangle.setAttribute(
        "fill-opacity",
        "0.78"
    );

    rectangle.setAttribute(
        "stroke",
        "#1e293b"
    );

    rectangle.setAttribute(
        "stroke-width",
        "3"
    );

    svg.appendChild(rectangle);

    addRoomLabel(
        namespace,
        room,
        x,
        y,
        width,
        height
    );

    addDoor(
        namespace,
        x,
        y,
        width,
        height,
        index
    );

    addWindows(
        namespace,
        x,
        y,
        width,
        height
    );
}


function addRoomLabel(
    namespace,
    room,
    x,
    y,
    width,
    height
) {
    const name =
        document.createElementNS(
            namespace,
            "text"
        );

    name.setAttribute(
        "x",
        x + width / 2
    );

    name.setAttribute(
        "y",
        y + height / 2 - 9
    );

    name.setAttribute(
        "text-anchor",
        "middle"
    );

    name.setAttribute(
        "font-size",
        "15"
    );

    name.setAttribute(
        "font-weight",
        "700"
    );

    name.setAttribute(
        "fill",
        "#0f172a"
    );

    name.textContent = room.name;

    svg.appendChild(name);

    const dimensions =
        document.createElementNS(
            namespace,
            "text"
        );

    dimensions.setAttribute(
        "x",
        x + width / 2
    );

    dimensions.setAttribute(
        "y",
        y + height / 2 + 14
    );

    dimensions.setAttribute(
        "text-anchor",
        "middle"
    );

    dimensions.setAttribute(
        "font-size",
        "11"
    );

    dimensions.setAttribute(
        "fill",
        "#334155"
    );

    dimensions.textContent =
        `${room.width} ft × ${room.length} ft`;

    svg.appendChild(dimensions);

    const area =
        document.createElementNS(
            namespace,
            "text"
        );

    area.setAttribute(
        "x",
        x + width / 2
    );

    area.setAttribute(
        "y",
        y + height / 2 + 32
    );

    area.setAttribute(
        "text-anchor",
        "middle"
    );

    area.setAttribute(
        "font-size",
        "10"
    );

    area.setAttribute(
        "fill",
        "#475569"
    );

    area.textContent =
        `${room.area} sq.ft`;

    svg.appendChild(area);
}


function addDoor(
    namespace,
    x,
    y,
    width,
    height,
    index
) {
    const doorWidth =
        Math.min(34, width * 0.25);

    const door =
        document.createElementNS(
            namespace,
            "line"
        );

    if (index % 2 === 0) {
        door.setAttribute(
            "x1",
            x + width / 2 - doorWidth / 2
        );

        door.setAttribute(
            "y1",
            y + height
        );

        door.setAttribute(
            "x2",
            x + width / 2 + doorWidth / 2
        );

        door.setAttribute(
            "y2",
            y + height
        );
    } else {
        door.setAttribute(
            "x1",
            x
        );

        door.setAttribute(
            "y1",
            y + height / 2 - doorWidth / 2
        );

        door.setAttribute(
            "x2",
            x
        );

        door.setAttribute(
            "y2",
            y + height / 2 + doorWidth / 2
        );
    }

    door.setAttribute(
        "stroke",
        "#ffffff"
    );

    door.setAttribute(
        "stroke-width",
        "7"
    );

    svg.appendChild(door);
}


function addWindows(
    namespace,
    x,
    y,
    width,
    height
) {
    if (width < 70 || height < 60) {
        return;
    }

    const windowLine =
        document.createElementNS(
            namespace,
            "line"
        );

    windowLine.setAttribute(
        "x1",
        x + width * 0.3
    );

    windowLine.setAttribute(
        "y1",
        y
    );

    windowLine.setAttribute(
        "x2",
        x + width * 0.7
    );

    windowLine.setAttribute(
        "y2",
        y
    );

    windowLine.setAttribute(
        "stroke",
        "#0284c7"
    );

    windowLine.setAttribute(
        "stroke-width",
        "7"
    );

    svg.appendChild(windowLine);
}


function addPlotDimensions(
    namespace,
    blueprint,
    x,
    y,
    width,
    height
) {
    const widthText =
        document.createElementNS(
            namespace,
            "text"
        );

    widthText.setAttribute(
        "x",
        x + width / 2
    );

    widthText.setAttribute(
        "y",
        y + height + 36
    );

    widthText.setAttribute(
        "text-anchor",
        "middle"
    );

    widthText.setAttribute(
        "font-size",
        "14"
    );

    widthText.setAttribute(
        "font-weight",
        "700"
    );

    widthText.textContent =
        `Plot Width: ${blueprint.plot.width} ft`;

    svg.appendChild(widthText);

    const lengthText =
        document.createElementNS(
            namespace,
            "text"
        );

    lengthText.setAttribute(
        "x",
        x - 35
    );

    lengthText.setAttribute(
        "y",
        y + height / 2
    );

    lengthText.setAttribute(
        "text-anchor",
        "middle"
    );

    lengthText.setAttribute(
        "font-size",
        "14"
    );

    lengthText.setAttribute(
        "font-weight",
        "700"
    );

    lengthText.setAttribute(
        "transform",
        `rotate(-90 ${x - 35} ${y + height / 2})`
    );

    lengthText.textContent =
        `Plot Length: ${blueprint.plot.length} ft`;

    svg.appendChild(lengthText);
}


function addNorthArrow(namespace) {
    const arrow =
        document.createElementNS(
            namespace,
            "text"
        );

    arrow.setAttribute("x", "830");
    arrow.setAttribute("y", "75");
    arrow.setAttribute(
        "text-anchor",
        "middle"
    );

    arrow.setAttribute(
        "font-size",
        "24"
    );

    arrow.setAttribute(
        "font-weight",
        "700"
    );

    arrow.textContent = "↑ N";

    svg.appendChild(arrow);
}


function updateStatistics(blueprint) {
    document.getElementById(
        "totalArea"
    ).textContent =
        `${blueprint.plot.area} sq.ft`;

    document.getElementById(
        "totalRooms"
    ).textContent =
        blueprint.layout.total_rooms;

    document.getElementById(
        "plotSize"
    ).textContent =
        `${blueprint.plot.width} × ${blueprint.plot.length} ft`;

    document.getElementById(
        "floorCount"
    ).textContent =
        document.getElementById(
            "floors"
        ).value;
}


function createLegend(rooms) {
    const legendItems =
        document.getElementById(
            "legendItems"
        );

    legendItems.innerHTML = "";

    const uniqueNames = [
        ...new Set(
            rooms.map(
                room =>
                    getRoomCategory(room.name)
            )
        )
    ];

    uniqueNames.forEach(category => {
        const item =
            document.createElement("div");

        item.className = "legend-item";

        item.innerHTML = `
            <span
                class="legend-color"
                style="background:${getRoomColor(category)}"
            ></span>
            <span>${category}</span>
        `;

        legendItems.appendChild(item);
    });
}


function getRoomCategory(name) {
    if (name.includes("Bedroom")) {
        return "Bedroom";
    }

    if (name.includes("Bathroom")) {
        return "Bathroom";
    }

    return name;
}


function getRoomColor(name) {
    if (name.includes("Living")) {
        return "#bfdbfe";
    }

    if (name.includes("Kitchen")) {
        return "#fde68a";
    }

    if (name.includes("Bedroom")) {
        return "#ddd6fe";
    }

    if (name.includes("Bathroom")) {
        return "#a5f3fc";
    }

    if (name.includes("Parking")) {
        return "#cbd5e1";
    }

    if (name.includes("Balcony")) {
        return "#bbf7d0";
    }

    if (name.includes("Dining")) {
        return "#fed7aa";
    }

    if (name.includes("Study")) {
        return "#fecdd3";
    }

    return "#e2e8f0";
}


function clearBlueprint() {
    svg.innerHTML = "";
    svg.style.display = "none";

    emptyState.style.display = "flex";

    statistics.classList.add("hidden");
    legend.classList.add("hidden");

    downloadButton.disabled = true;

    message.textContent = "";
}


function downloadBlueprint() {
    if (!svg.innerHTML.trim()) {
        return;
    }

    const serializer =
        new XMLSerializer();

    let source =
        serializer.serializeToString(svg);

    if (
        !source.includes(
            'xmlns="http://www.w3.org/2000/svg"'
        )
    ) {
        source = source.replace(
            "<svg",
            '<svg xmlns="http://www.w3.org/2000/svg"'
        );
    }

    const blob =
        new Blob(
            [source],
            {
                type: "image/svg+xml"
            }
        );

    const url =
        URL.createObjectURL(blob);

    const link =
        document.createElement("a");

    const projectName =
        document.getElementById(
            "projectName"
        ).value.trim() ||
        "blueprint";

    link.href = url;

    link.download =
        `${projectName.replaceAll(" ", "-")}.svg`;

    link.click();

    URL.revokeObjectURL(url);
}