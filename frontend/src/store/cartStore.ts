import { create } from 'zustand';
import { Cart, CartItem } from '@/types';

interface CartState {
  cart: Cart | null;
  setCart: (cart: Cart | null) => void;
  addItem: (item: CartItem) => void;
  removeItem: (itemId: string) => void;
  updateQuantity: (itemId: string, quantity: number) => void;
  clearCart: () => void;
}

export const useCartStore = create<CartState>((set) => ({
  cart: null,
  setCart: (cart) => set({ cart }),
  addItem: (item) =>
    set((state) => {
      if (!state.cart) return state;
      const existingItem = state.cart.items.find((i) => i.product_id === item.product_id);
      if (existingItem) {
        return {
          cart: {
            ...state.cart,
            items: state.cart.items.map((i) =>
              i.product_id === item.product_id
                ? { ...i, quantity: i.quantity + item.quantity }
                : i
            ),
          },
        };
      }
      return {
        cart: {
          ...state.cart,
          items: [...state.cart.items, item],
        },
      };
    }),
  removeItem: (itemId) =>
    set((state) => {
      if (!state.cart) return state;
      return {
        cart: {
          ...state.cart,
          items: state.cart.items.filter((item) => item.id !== itemId),
        },
      };
    }),
  updateQuantity: (itemId, quantity) =>
    set((state) => {
      if (!state.cart) return state;
      return {
        cart: {
          ...state.cart,
          items: state.cart.items.map((item) =>
            item.id === itemId ? { ...item, quantity } : item
          ),
        },
      };
    }),
  clearCart: () => set({ cart: null }),
}));
