// static/js/home.js

function setTab(el) {
  document.querySelectorAll('.feed-tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
}

function toggleLike(btn) {
  const span = btn.querySelector('span');
  const svg  = btn.querySelector('svg');
  const isLiked = btn.classList.toggle('liked');
  const count = parseInt(span.textContent);
  span.textContent = isLiked ? count + 1 : count - 1;
  svg.setAttribute('fill',   isLiked ? '#e05252' : 'none');
  svg.setAttribute('stroke', isLiked ? '#e05252' : 'currentColor');
}

function toggleComments(btn) {
  const section = btn.closest('.post-card').querySelector('.comments-section');
  section.classList.toggle('open');
}

function toggleFollow(btn) {
  const isFollowing = btn.classList.toggle('following');
  btn.textContent = isFollowing ? 'Following' : 'Follow';
}

function toggleFollowSidebar(btn) {
  const isFollowing = btn.classList.toggle('following');
  btn.textContent = isFollowing ? 'Following' : 'Follow';
}