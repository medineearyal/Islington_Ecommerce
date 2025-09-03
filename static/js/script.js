document.body.addEventListener("htmx:afterSwap", (event) => {
    if (event.detail.target.id === "quick-view-container") {
        const modalContainer = document.getElementById("quick-view-container");
        const modal = modalContainer.querySelector("dialog");
        if (modal) {
            modal.showModal();
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
        }
    }
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

    const swiper = new Swiper('.main-category-swiper', {
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
            nextEl: '.main-category-swiper-wrapper .swiper-button-next',
            prevEl: '.main-category-swiper-wrapper .swiper-button-prev',
        },

        breakpoints: {
            320: {
                slidesPerView: 1.3,
                spaceBetween: 16,
            },
            375: {
                slidesPerView: 1.5,
                spaceBetween: 16,
            },
            425: {
                slidesPerView: 1.75,
            },
            640: {
                slidesPerView: 3.5,
                spaceBetween: 20
            },
            1024: {
                slidesPerView: 4.75,
                spaceBetween: 40
            },
            1440: {
                slidesPerView: 6,
            }
        }
    });

    const featuredSwiper = new Swiper(".featured-swiper", {
        direction: "horizontal",
        speed: 500,
        loop: true,
        slidesPerView: 1,

        pagination: {
            el: ".swiper-pagination"
        },

        autoplay: {
            delay: 3000,
            disableOnInteraction: true
        },
        navigation: {
            nextEl: ".featured-swiper .swiper-button-next",
            prevEl: ".featured_swiper .swiper-button-prev"
        }
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

    const noticeSwiper = new Swiper(".notice-swiper", {
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

    document.body.addEventListener("htmx:afterSwap", (e) => {
        const form = e.target.querySelector("#product-attribute-form");
        if (!form) return;

        form.removeEventListener("submit", handleAttributeFormSubmit);
        form.addEventListener("submit", handleAttributeFormSubmit);
    });

    async function handleAttributeFormSubmit(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: form.method,
                body: formData
            });
            const data = await response.json();

            if (data.id) {
                const select = document.querySelector("#attributes-formset select:last-of-type");
                const option = new Option(data.name, data.id, true, true);
                select.add(option);

                const input = document.getElementById("new-attr-name");
                if (input) input.value = "";
                const toggle = document.getElementById("attr-modal-toggle");
                if (toggle) toggle.checked = false;
            } else if (data.errors) {
                console.log("Validation errors:", data.errors);
            }
        } catch (err) {
            console.error("AJAX error:", err);
        }
    }
});

document.body.addEventListener("showMessage", function (event) {
    const container = document.getElementById("message-container");
    let toastMessage = `
        <div class="toast toast-top toast-end z-9">
            <div class="relative alert ${event.detail.tag} fade-out" role="alert">
                <span id="toast-message">${event.detail.text}</span>
                <div class="absolute bottom-0 left-0 h-1 bg-current progress-bar"></div>
            </div>
        </div>
    `;
    container.innerHTML = toastMessage;
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

    if (currentValue > Number(stockElem.getAttribute("min"))) {
        stockElem.value = currentValue - 1;
        stockElem.dispatchEvent(new Event("change", {bubbles: true}));
    }
}

function increaseStock(elem) {
    const stockElem = elem.parentElement.parentElement.querySelector("input[type=number]");
    const currentValue = Number(stockElem.value);

    if (currentValue < Number(stockElem.getAttribute("max"))) {
        stockElem.value = currentValue + 1;
        stockElem.dispatchEvent(new Event("change", {bubbles: true}));
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
    } else {
        if (stockError && cartBtn) {
            stockError.classList.add("hidden");
            cartBtn.removeAttribute("disabled");

            const addToCartBtn = document.querySelector("#add-to-cart");
            const hxGet = addToCartBtn.getAttribute("hx-get");
            let urlParams = new URLSearchParams(hxGet.split("?")[1]);
            urlParams.set("quantity", currentValue);
            const newHxGet = hxGet.split("?")[0] + "?" + urlParams.toString();
            addToCartBtn.setAttribute("hx-get", newHxGet);
            htmx.process(addToCartBtn);
        }

        const priceElem = document.getElementById(elem.getAttribute("data-price-container"));
        const price = Number(elem.getAttribute("data-price"));
        if (priceElem && price) {
            priceElem.innerHTML = `Rs. ${currentValue * price}`;
            const updateUrl = `${elem.getAttribute("data-url")}&quantity=${currentValue}`;
            window.location.href = updateUrl;
        }
    }
}

function showStep(index) {
    steps.forEach((step, i) => {
        const el = document.getElementById(step.id);
        if (i === index) el.classList.remove("hidden");
        else el.classList.add("hidden");
    });

    stepName.textContent = steps[index].name;

    progressBar.style.width = steps[index].percent + "%";
}

function setupDynamicFormset(opts) {
    const {prefix, addBtnId, containerId, templateId} = opts;
    const totalInput = document.querySelector(`#id_${prefix}-TOTAL_FORMS`);
    const addBtn = document.getElementById(addBtnId);
    const container = document.getElementById(containerId);
    const tmplHTML = document.getElementById(templateId).innerHTML.trim();

    function addForm() {
        const index = parseInt(totalInput.value, 10);
        const html = tmplHTML.replace(/__prefix__/g, index);
        container.insertAdjacentHTML("beforeend", html);
        totalInput.value = index + 1;
    }

    addBtn?.addEventListener("click", addForm);

    container.addEventListener("click", (e) => {
        if (e.target.closest('[data-action="remove-form"]')) {
            const block = e.target.closest("[data-formset-item]");
            const del = block.querySelector('input[type="checkbox"][name$="-DELETE"]');
            if (del) del.checked = true;
            block.style.display = "none";
        }
    });
}