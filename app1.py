</form>
<div class="response" id="statsResponse"></div>
</section>

        <!-- Redirect -->
        <section>
            <h2>Test Redirect</h2>
            <form id="redirectForm">
                <input type="text" id="redirectCode" placeholder="Enter short code" required>
                <button type="submit">Go</button>
            </form>
        </section>
</div>

        


<script>

        // Redirect
        document.getElementById("redirectForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            const code = document.getElementById("redirectCode").value;
            window.location.href = `/r/${code}`;
        });
        
// Create
document.getElementById("createForm").addEventListener("submit", async (e) => {
e.preventDefault();
