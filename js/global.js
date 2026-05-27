// * HEADER
const btnBars = document.querySelector('.btn-bars');
const menuResponsive = document.querySelector('.menu-responsive');
const btnClose = document.querySelector('.btn-close');

if (btnBars && menuResponsive) {
	btnBars.addEventListener('click', () => {
		menuResponsive.classList.toggle('active');
		document.body.classList.toggle('no-scroll');
	});
}

if (btnClose && menuResponsive) {
	btnClose.addEventListener('click', () => {
		menuResponsive.classList.remove('active');
		document.body.classList.remove('no-scroll');
	});
}

// * VIEWPORT PREVIEW
const viewportToggle = document.querySelector('.viewport-toggle');
const viewportToggleIcon = viewportToggle?.querySelector('i');
const viewportToggleText = viewportToggle?.querySelector('.viewport-toggle__text');
const viewportModeKey = 'adventureroViewportMode';

if (viewportToggle) {
	const previewShell = document.createElement('div');
	const previewContent = document.createElement('div');

	previewShell.className = 'mobile-preview-shell';
	previewContent.className = 'mobile-preview-content';
	previewShell.appendChild(previewContent);

	Array.from(document.body.children).forEach(element => {
		if (element !== viewportToggle && !element.classList.contains('travel-chatbot')) {
			previewContent.appendChild(element);
		}
	});

	document.body.insertBefore(previewShell, viewportToggle);

	const setToggleState = mode => {
		const isMobile = mode === 'mobile';

		viewportToggle.setAttribute('aria-pressed', String(isMobile));
		viewportToggleText.textContent = isMobile ? 'Mobile' : 'Desktop';
		viewportToggleIcon.className = isMobile ? 'fa-solid fa-mobile-screen-button' : 'fa-solid fa-desktop';
	};

	const applyViewportMode = mode => {
		localStorage.setItem(viewportModeKey, mode);
		setToggleState(mode);
		document.body.classList.toggle('mobile-preview', mode === 'mobile');
		document.body.classList.toggle('desktop-preview', mode !== 'mobile');
	};

	const savedMode = localStorage.getItem(viewportModeKey) === 'mobile' ? 'mobile' : 'desktop';
	applyViewportMode(savedMode);

	viewportToggle.addEventListener('click', () => {
		const nextMode = localStorage.getItem(viewportModeKey) === 'mobile' ? 'desktop' : 'mobile';
		applyViewportMode(nextMode);
	});
}

// * TRAVEL CHATBOT
const chatbot = document.querySelector('.travel-chatbot');
const chatbotToggle = chatbot?.querySelector('.chatbot-toggle');
const chatbotClose = chatbot?.querySelector('.chatbot-close');
const chatbotMessages = chatbot?.querySelector('.chatbot-messages');
const chatbotForm = chatbot?.querySelector('.chatbot-form');
const chatbotInput = chatbot?.querySelector('#chatbot-input');
const chatbotQuickActions = chatbot?.querySelectorAll('[data-chat-message]');
const chatbotHistoryKey = 'adventureroChatHistory';

if (chatbot && chatbotToggle && chatbotMessages && chatbotForm && chatbotInput) {
	const defaultBotMessage = {
		role: 'bot',
		text: 'Hola, soy Adventurero Bot. Puedo ayudarte con tours, reservas, contacto y metodos de pago.',
	};

	const getStoredMessages = () => {
		try {
			const messages = JSON.parse(localStorage.getItem(chatbotHistoryKey));
			return Array.isArray(messages) && messages.length ? messages : [defaultBotMessage];
		} catch (error) {
			return [defaultBotMessage];
		}
	};

	let chatbotHistory = getStoredMessages();

	const saveChatbotHistory = () => {
		localStorage.setItem(chatbotHistoryKey, JSON.stringify(chatbotHistory.slice(-24)));
	};

	const scrollChatToBottom = () => {
		chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
	};

	const renderMessage = ({ role, text }) => {
		const message = document.createElement('div');
		message.className = `chatbot-message ${role}`;
		message.textContent = text;
		chatbotMessages.appendChild(message);
		scrollChatToBottom();
		return message;
	};

	const renderHistory = () => {
		chatbotMessages.innerHTML = '';
		chatbotHistory.forEach(renderMessage);
	};

	const addMessage = (role, text) => {
		const message = { role, text };
		chatbotHistory.push(message);
		saveChatbotHistory();
		renderMessage(message);
	};

	const showTyping = () => {
		const typing = document.createElement('div');
		typing.className = 'chatbot-message bot typing';
		typing.innerHTML = '<span></span><span></span><span></span>';
		chatbotMessages.appendChild(typing);
		scrollChatToBottom();
		return typing;
	};

	const normalizeText = text =>
		text
			.toLowerCase()
			.normalize('NFD')
			.replace(/[\u0300-\u036f]/g, '');

	const scrollToTarget = selector => {
		const target = document.querySelector(selector);

		if (!target) return false;

		target.scrollIntoView({ behavior: 'smooth', block: 'start' });
		return true;
	};

	const findChatbotResponse = message => {
		const text = normalizeText(message);

		if (text.includes('tour') || text.includes('paquete') || text.includes('viaje')) {
			return {
				text: 'Te muestro nuestros tours disponibles. Alli puedes comparar destinos, duracion, capacidad y precios.',
				target: '#travel-tours',
				fallback: 'Si quieres reservar, abre el detalle del tour que mas te guste.',
			};
		}

		if (text.includes('contact') || text.includes('telefono') || text.includes('correo') || text.includes('direccion')) {
			return {
				text: 'Aqui tienes nuestros datos de contacto para hablar con el equipo de Adventurero.',
				target: '#travel-contact',
			};
		}

		if (text.includes('pago') || text.includes('metodo') || text.includes('tarjeta') || text.includes('metodos')) {
			return {
				text: 'Estos son los metodos de pago disponibles para tus reservas.',
				target: '#travel-payments',
			};
		}

		if (text.includes('reserv') || text.includes('booking') || text.includes('comprar')) {
			return {
				text: 'Para reservar, elige un tour y usa el boton de reserva. Si ya estas en el detalle, te llevo al formulario o boton correspondiente.',
				target: '#travel-booking',
				fallback: 'No veo un formulario de reserva en esta pagina, pero te acerco a los tours para que elijas uno.',
				fallbackTarget: '#travel-tours',
			};
		}

		if (text.includes('hola') || text.includes('ayuda') || text.includes('buenas')) {
			return {
				text: 'Claro. Puedes preguntarme por tours, contacto, reservas o metodos de pago. Tambien puedes usar los botones rapidos.',
			};
		}

		return {
			text: 'Puedo ayudarte con tours, contacto, reservas y pagos. Prueba escribiendo “tours”, “contacto”, “reservar” o “pagos”.',
		};
	};

	const answerMessage = message => {
		const response = findChatbotResponse(message);
		const typing = showTyping();

		window.setTimeout(() => {
			typing.remove();

			let finalText = response.text;
			const foundTarget = response.target ? scrollToTarget(response.target) : false;

			if (!foundTarget && response.fallbackTarget) {
				scrollToTarget(response.fallbackTarget);
				finalText = `${response.text} ${response.fallback}`;
			} else if (!foundTarget && response.fallback) {
				finalText = `${response.text} ${response.fallback}`;
			}

			addMessage('bot', finalText);
		}, 650);
	};

	const submitChatbotMessage = message => {
		const cleanMessage = message.trim();

		if (!cleanMessage) return;

		addMessage('user', cleanMessage);
		chatbotInput.value = '';
		answerMessage(cleanMessage);
	};

	renderHistory();

	chatbotToggle.addEventListener('click', () => {
		chatbot.classList.toggle('chatbot-open');
		chatbotToggle.setAttribute('aria-expanded', String(chatbot.classList.contains('chatbot-open')));

		if (chatbot.classList.contains('chatbot-open')) {
			window.setTimeout(() => chatbotInput.focus(), 180);
			scrollChatToBottom();
		}
	});

	chatbotClose?.addEventListener('click', () => {
		chatbot.classList.remove('chatbot-open');
		chatbotToggle.setAttribute('aria-expanded', 'false');
	});

	chatbotForm.addEventListener('submit', event => {
		event.preventDefault();
		submitChatbotMessage(chatbotInput.value);
	});

	chatbotQuickActions.forEach(button => {
		button.addEventListener('click', () => {
			submitChatbotMessage(button.dataset.chatMessage || button.textContent);
		});
	});
}
