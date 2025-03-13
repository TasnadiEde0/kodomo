window.onload = async () => {
    //Logout

    const logoutButton = document.getElementById('navbar--logout-button');

    if(logoutButton) {
        logoutButton.addEventListener('click', function () {
            fetch('/logout', {
                method: 'POST'
            })
                .then(response => {
                    if (response.ok) {
                        window.location.href = '/login';
                    } else {
                        console.error('Request failed:', response.status);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            window.location.href = '/login';
        });
    }

    //Render
    const DAY_COORD_LEN = 30;
    const LEFT_PADDING = 20;
    const RIGHT_PADDING = 100;

    const container = document.getElementById('scrollable-container');
    const errorPar = document.querySelector('.scrollable-error');
    const accDeleteButton = document.getElementById("footer--del-acc__button");

    if(accDeleteButton) {
        accDeleteButton.addEventListener('click', function () {
            if(confirm("Are you sure you want to delete your account?")) {
                fetch('/api/user', {
                    method: 'DELETE'
                })
                    .then(response => {
                        if (response.ok) {
                            window.location.href = '/login';
                        } else {
                            console.error('Request failed:', response.status);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                window.location.href = '/login';
            }
        });
    }

    let periods = [];
    let imgs = [];

    await fetch('/api/periods', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch periods.');
        }
        return response.json();
    })
    .then(data => {
        console.log('Periods:', data);
        periods = data;
        console.log(periods);
    })
    .catch(error => {
        errorPar.textContent = error;
        console.error('Error:', error);
    });

    await fetch('/api/images', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch images.');
        }
        return response.json();
    })
    .then(data => {
        console.log('Images:', data);
        imgs = data;
    })
    .catch(error => {
        errorPar.textContent = error;
        console.error('Error:', error);
    });

    if (periods.length !== 0 && imgs.length !== 0) {


        periods.sort((a, b) => new Date(a.date) - new Date(b.date));
        imgs.sort((a, b) => new Date(a.start) - new Date(b.start));

        const canvas = document.querySelector('.scrollable-canvas');
        canvas.width = 5000;
        canvas.height = 500;
        const ctx = canvas.getContext('2d');

        let earliestDate = periods[0].start;
        imgs.map(img => {
            if (new Date(img.date) < new Date(earliestDate)) {
                earliestDate = img.date;
            }
        })

        let currHigh = new Date();
        let currLow = new Date();
        if (new Date(earliestDate) < new Date(periods[0].start)) {
            const last = new Date(periods[0].start);
            currHigh = new Date(last);
            currHigh.setDate(currHigh.getDate() - 14);
            currLow = new Date(last);
            currLow.setDate(currLow.getDate() - 28);

            while (new Date(earliestDate) < currLow) {
                currHigh.setDate(currHigh.getDate() - 28);
                currLow.setDate(currLow.getDate() - 28);
            }
            earliestDate = currLow.toDateString()
        }


        function dateToX(dateStr) {
            const startDate = new Date(earliestDate);
            const currentDate = new Date(dateStr);
            const diffDays = Math.ceil((currentDate - startDate + LEFT_PADDING) / (1000 * 60 * 60 * 24));
            return diffDays * DAY_COORD_LEN;
        }

        function drawCurve(periods) {
            const half_points = periods.map(period => ({
                x: (dateToX(period.start) + dateToX(period.end)) / 2,
                y: 400
            }));

            for (let i = 0; i < half_points.length - 1; i++) {
                const gap = half_points[i + 1].x - half_points[i].x;
                if (gap > 40 * DAY_COORD_LEN) {
                    const midpoint = (half_points[i].x + half_points[i + 1].x) / 2;
                    half_points.splice(i + 1, 0, { x: midpoint, y: 400 });
                }
            }

            const points = [];

            for (let i = 0; i < half_points.length - 1; i++) {
                const midpoint = (half_points[i + 1].x + half_points[i].x) / 2;

                points.push({x: half_points[i].x, y: half_points[i].y});
                points.push({x: midpoint, y: 100});
            }
            points.push({x: half_points[half_points.length - 1].x, y: half_points[half_points.length - 1].y});

            const finalPer = new Date((new Date(periods[periods.length - 1].start).getTime() + new Date(periods[periods.length - 1].end).getTime()) / 2 );

            console.log(finalPer)

            if (new Date(imgs[imgs.length - 1].date) - finalPer > 1000 * 12) {
                const last = new Date(imgs[imgs.length - 1].date);
                let currHigh = new Date(finalPer);
                currHigh.setDate(currHigh.getDate() + 14);
                let currLow = new Date(finalPer);
                currLow.setDate(currLow.getDate() + 28);

                points.push({ x: dateToX(currHigh), y: 100 });
                points.push({ x: dateToX(currLow), y: 400 });

                while (last > currLow) {
                    currHigh.setDate(currHigh.getDate() + 28);
                    currLow.setDate(currLow.getDate() + 28);

                    points.push({ x: dateToX(currHigh), y: 100 });
                    points.push({ x: dateToX(currLow), y: 400 });
                }
            }

            if (new Date(earliestDate) < new Date(periods[0].start)) {
                const last = new Date(periods[0].start + "T00:00:00");
                let currHigh = new Date(last);
                currHigh.setDate(currHigh.getDate() - 14);
                let currLow = new Date(last);
                currLow.setDate(currLow.getDate() - 28);

                points.unshift({ x: dateToX(currHigh), y: 100 });
                points.unshift({ x: dateToX(currLow), y: 400 });

                while (new Date(earliestDate) < currLow) {
                    currHigh.setDate(currHigh.getDate() - 28);
                    currLow.setDate(currLow.getDate() - 28);

                    points.unshift({ x: dateToX(currHigh), y: 100 });
                    points.unshift({ x: dateToX(currLow), y: 400 });
                }
            }

            canvas.width = points[points.length - 1].x + RIGHT_PADDING;

            console.log(points)

            ctx.strokeStyle = 'black';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(points[0].x, points[0].y);

            for (let i = 0; i < points.length - 1; i++) {
                const cp1x = (points[i].x + points[i + 1].x) / 2;
                const cp1y = points[i].y;
                const cp2x = (points[i].x + points[i + 1].x) / 2;
                const cp2y = points[i + 1].y;

                ctx.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, points[i + 1].x, points[i + 1].y);

                ctx.stroke();
            }
        }

        function drawDates(periods) {
            ctx.font = "12px Arial";
            ctx.fillStyle = "black";
            ctx.textAlign = "center";

            periods.forEach(period => {
                const x = (dateToX(period.start) + dateToX(period.end)) / 2;
                ctx.fillText(`${period.start.replaceAll("-", ":")} - ${period.end.replaceAll("-", ":")}`, x, 470);
            });
        }

        function drawImages(imgs) {
            imgs.forEach(img => {
                console.log(img)
                const imgX = dateToX(img.date);
                const imgY = 400 - img.prob * 300;
                const image = new Image();

                image.src = img.imagePath;
                image.onload = () => {
                    ctx.drawImage(image, LEFT_PADDING + imgX - 15, imgY - 15, 30, 30);

                    canvas.addEventListener('click', (e) => {
                        const rect = canvas.getBoundingClientRect();
                        const clickX = e.clientX - rect.left;
                        const clickY = e.clientY - rect.top;

                        if (clickX >= LEFT_PADDING + imgX - 15 && clickX <= LEFT_PADDING + imgX + 15 && clickY >= imgY - 15 && clickY <= imgY + 15) {
                            window.location.href = img.link;
                        }
                    });
                };
            });
        }

        drawCurve(periods);
        drawDates(periods);
        drawImages(imgs);

        container.scrollTo(container.scrollWidth, 0);
    }
}
