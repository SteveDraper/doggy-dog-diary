import { expect, test } from "@playwright/test";

test("placeholder home screen", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Doggy Dog Diary" })).toBeVisible();
  await expect(page.getByText("Phase 0 · placeholder home")).toBeVisible();
});
