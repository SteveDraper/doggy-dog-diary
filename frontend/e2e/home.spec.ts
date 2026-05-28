import { expect, test } from "@playwright/test";

test("home screen lists dogs and opens profile", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Doggy Dog Diary" })).toBeVisible();

  await page.getByRole("button", { name: "Add dog" }).click();
  await page.getByLabel("Name").fill("Nico");
  await page.getByRole("button", { name: "Add", exact: true }).click();

  await expect(page.getByRole("link", { name: /Nico/i })).toBeVisible();

  await page.getByRole("button", { name: "Add dog" }).click();
  await page.getByLabel("Name").fill("Bella");
  await page.getByRole("button", { name: "Add", exact: true }).click();

  await expect(page.getByRole("link", { name: /Bella/i })).toBeVisible();

  await page.getByRole("link", { name: /Nico/i }).click();
  await expect(page.getByRole("heading", { name: "Nico" })).toBeVisible();
  await expect(page.getByText("No description yet.")).toBeVisible();

  await page.getByRole("button", { name: "Edit description" }).click();
  await page.getByLabel("Description").fill("Anxious around loud noises.");
  await page.getByRole("button", { name: "Save" }).click();
  await expect(page.getByText("Anxious around loud noises.")).toBeVisible();

  await page.getByRole("button", { name: "Edit kennel club registration" }).click();
  await page.getByLabel("Registration number").fill("KC123456");
  await page.getByLabel("Registering body").fill("The Kennel Club");
  await page.getByRole("button", { name: "Save" }).click();
  await expect(page.getByText("KC123456")).toBeVisible();
  await expect(page.getByText("The Kennel Club")).toBeVisible();

  await page.getByRole("button", { name: "Edit dog status" }).click();
  await page.getByLabel("Status").selectOption("deceased");
  await page.getByLabel("Status date").fill("2026-01-01");
  await page.getByRole("button", { name: "Save" }).click();
  await expect(page.getByText("Deceased")).toBeVisible();

  await page.getByRole("link", { name: "← Back to home" }).click();
  const tiles = page.getByRole("link", { name: /Nico|Bella/i });
  await expect(tiles.nth(0)).toContainText("Bella");
  await expect(tiles.nth(1)).toContainText("Nico");
});
