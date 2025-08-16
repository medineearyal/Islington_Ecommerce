const thumbSwiper = new Swiper(".thumb-swiper", {
    direction: 'horizontal',
    slidesPerView: 6,
    watchSlidesProgress: true,
    watchSlideVisibility: true,
})

const productMainSwiper = new Swiper(".product-main-swiper", {
    slidesPerView: 1,

    navigation: {
        nextEl: ".thumb-container .swiper-button-next",
        prevEl: ".thumb-container .swiper-button-prev",
    },

    thumbs: {
        swiper: thumbSwiper,
    }
})

const swiper = new Swiper('.swiper', {
    direction: 'horizontal',
    speed: 500,
    loop: true,
    slidesPerView: 6,

    pagination: {
        el: '.swiper-pagination',
    },

    autoplay: {
        delay: 5000,
        disableOnInteraction: true,
    },

    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
});

const swiperBanner = new Swiper(".swiper-banner", {
    direction: 'horizontal',
    loop: true,
    speed: 500,
    slidesPerView: 1,

    autoplay: {
        delay: 5000,
        disableOnInteraction: true,
    },

    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
});

window.addEventListener("DOMContentLoaded", function () {
    const copyrightDate = document.querySelector(".copyright-date");
    if (copyrightDate) {
        copyrightDate.innerHTML = new Date().getFullYear();
    } else {
        copyrightDate.innerHTML = "2025";
    }

    const bestDealRemainingTime = document.getElementById("best-deal-remaining-time");
    if (bestDealRemainingTime) {
        const dealEndTimeIso = bestDealRemainingTime.getAttribute("data-end-date");
        const dealEndTime = new Date(dealEndTimeIso).getTime();

        function updateCountdown(countdownElem, dealEndTime) {
            const now = new Date().getTime();
            let distance = dealEndTime - now;

            if (distance <= 0) {
                countdownElem.innerHTML = "Expired";
                clearInterval(timer);
                return;
            }

            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);

            countdownElem.innerHTML = `${days}d : ${hours}h : ${minutes}m : ${seconds}s`;
        }

        updateCountdown(bestDealRemainingTime, dealEndTime);

        const timer = setInterval(() => updateCountdown(bestDealRemainingTime, dealEndTime), 1000);
    }

    const slider = document.getElementById('slider');
    if (slider) {
        const minOutput = document.getElementById('slider-min');
        const maxOutput = document.getElementById('slider-max');

        const minPrice = Number(minOutput.getAttribute("data-min-price")) || 0;
        const maxPrice = Number(maxOutput.getAttribute("data-max-price")) || 0;


        noUiSlider.create(slider, {
            start: [
                minPrice + 10000, maxPrice - 10000
            ],
            connect: true,
            range: {
                'min': minPrice,
                'max': maxPrice
            },
            step: 1000,
            tooltips: [true, true],
            format: {
                to: value => Math.round(value),
                from: value => Math.round(value)
            }
        });

        slider.noUiSlider.on('change', function (values) {
            minOutput.value = values[0];
            maxOutput.value = values[1];
        });
    }

    const searchFilterForm = document.getElementById("search-filter-form");
    if (searchFilterForm) {
        searchFilterForm.addEventListener("submit", function (e) {
            const minField = searchFilterForm.querySelector("[name=min-price]");
            const maxField = searchFilterForm.querySelector("[name=max-price]");

            const minPrice = Number(minField?.value) || 0;
            const maxPrice = Number(maxField?.value) || 0;

            if (minPrice > maxPrice) {
                e.preventDefault();

                const error = document.getElementById("price-range-error");
                error.classList.add("block");
                error.classList.remove("hidden");
                error.innerHTML = "Max Price Cannot Be Smaller Than Min Price";
            }

            const urlParms = new URLSearchParams(window.location.search);
            const minPrevPrice = urlParms.get("min-price");
            const maxPrevPrice = urlParms.get("max-price");

            if (minPrice === 0 && maxPrice === 0) {
                if (minPrevPrice && maxPrevPrice) {
                    minField.value = minPrevPrice;
                    maxField.value = maxPrevPrice;
                }
            }
        })
    }
});

function priceReset(elem) {
    const minPriceInput = document.querySelector("[name=min_price]");
    const maxPriceInput = document.querySelector("[name=max_price]");

    minPriceInput.value = 0;
    maxPriceInput.value = 0;
}

function decreaseStock(elem) {
    const stockElem = elem.parentElement.parentElement.querySelector("input[type=number]");
    const currentValue = Number(stockElem.value);

    if (currentValue < Number(elem.getAttribute("min"))) {
        stockElem.value = currentValue - 1;
    }
}

function increaseStock(elem) {
    const stockElem = elem.parentElement.parentElement.querySelector("input[type=number]");
    const currentValue = Number(stockElem.value);

    if (currentValue < Number(elem.getAttribute("max"))) {
        stockElem.value = currentValue + 1;
    }
}

function checkForStockOverflow(elem) {
    const currentValue = Number(elem.value);
    const parent = elem.parentElement.parentElement;
    const stockError = parent.querySelector(".stock-error");
    const cartBtn = parent.querySelector(".cart-icon");

    if (currentValue > Number(elem.getAttribute("max"))) {
        stockError.classList.remove("hidden");
        cartBtn.setAttribute("disabled", "disabled");
    }else {
        stockError.classList.add("hidden");
        cartBtn.removeAttribute("disabled");
    }
}

function addToCart() {

}